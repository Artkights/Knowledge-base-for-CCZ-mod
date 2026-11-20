# 资料入库：突破攻击 / 盾墙防突破 / 偷袭攻击 —— 三份 QQ 资料

> 来源：`6.3突破攻击【代码解析】【效果修改】【技能拓展】——by普罗.docx`、`盾墙防突破版.txt`、`偷袭攻击分析.docx`（用户提供，2026-10-18 全文入库）
> 版本提示：6.3/6.x 资料；本库已在 6.6 样本逐条核对（见 `03-机制详解\突破攻击-盾墙-偷袭-6.3文档与6.6映射.md`）。

## 一、6.3 突破攻击（by 普罗）

6.3突破攻击【代码解析】【效果修改】【技能拓展】
最近研究了下突破攻击，因为突破攻击是我目前最喜欢的技能之一，把敌人打到后撤非常爽所以开了一个新帖，主要分享一下突破攻击技能代码的一点个人解读，以及一些修改和拓展的小技巧。一楼先介绍一下突破攻击的代码结构，主要是给其他反汇编同好大佬们快速了解结构，之后对突破攻击做优化或特技可以更快上手；在二楼会分享一点突破攻击相关的修改方式，例如修改击打后对话、修改特殊地形不击退等等内容。代码结构第一部分：分流加强攻击与突破攻击在6.3引擎中加强攻击和突破攻击已经成功分离为两个特技，但是在代码处两者依然是在一起的。因此第一部分代码的终极任务就是：判断攻击者拥有的是加强攻击技能，还是突破攻击技能，还是俩技能都没有，然后根据不同的情况跳转到不同的地址去。0041106D   $  55            push ebp0041106E   .  8BEC          mov ebp,esp00411070   .  51            push ecx00411071   .  68 F05D4B00   push Ekd54.004B5DF000411076   .  8B4D 10       mov ecx,dword ptr ss:[ebp+10]00411079   .  E8 1155FFFF   call Ekd54.0040658F           获取攻击者的Data地址0041107E   .  51            push ecx0041107F   .  83EC 0C       sub esp,0C00411082   .  6A 16         push 1600411084   .  FF35 9B0E5000 push dword ptr ds:[500E9B]0041108A   .  E8 03530200   call Ekd54.004363920041108F   .  85C0          test eax,eax00411091   .  75 18         jnz short Ekd54.004110AB00411093   .  8B4D F4       mov ecx,dword ptr ss:[ebp-C]00411096   .  E8 8F000100   call Ekd54.0042112A0041109B   .  84C0          test al,al                              检测技能是否为加强攻击，al=0表示不是加强攻击，al≠0表示是加强攻击0041109D   .  75 23         jnz short Ekd54.004110C2     开始分流，如果是加强攻击就去4110C2，如果不是则继续执行下面的代码0041109F   .  8B4D F4       mov ecx,dword ptr ss:[ebp-C]004110A2   .  E8 71000100   call Ekd54.00421118004110A7   .  85C0          test eax,eax                         检测技能是否为突破攻击，al=0表示不是（即既不是突破也不是加强），al≠0表示是突破攻击004110A9   .  74 29         je short Ekd54.004110D4       开始分流，如果既非突破也非加强就跳去4110D4，连着跳几次就结束子程序了；如果是突破攻击则继续执行下面的代码004110AB   >  803D 9A0E5000>cmp byte ptr ds:[500E9A],1004110B2   .  74 0C         je short Ekd54.004110C0004110B4   .  8B4D 0C       mov ecx,dword ptr ss:[ebp+C]004110B7   .  E8 775A0100   call Ekd54.00426B33004110BC   .  85C0          test eax,eax004110BE   .  74 16         je short Ekd54.004110D6       有突破攻击技能的话，就跳到4110D6那么接下来三种情况的分流去向也很明显了：加强攻击：去4110C2突破攻击：去4110D6啥也没有：去4110D4，紧接着jmp到411130，然后就结束子程序了第二部分：伤害加强计算首先很容易知道“伤害加强”这部分肯定是为加强攻击服务的，加强攻击跳转到4110C2这里就开始进行加成数值的计算。但是，这部分代码并不止为加强攻击服务，如果突破攻击没有造成敌人后退，那40%的伤害增益也会跳到这里进行计算。具体突破攻击在什么时机会跳到这里我在后文会解析到。004110C0   >  B0 28         mov al,28                                 突破攻击增益会跳到这里，这里设置al就是在设置突破攻击的伤害加成为40%004110C2   >  837D 08 01    cmp dword ptr ss:[ebp+8],1   加强攻击会跳到这里，在跳到这里之前al中已经存好了效果值，设定为30%那al就是30004110C6   .  74 0C         je short Ekd54.004110D4004110C8   .  50            push eax                                 004110C9   .  FF75 FC       push dword ptr ss:[ebp-4]          ebp-4中存储着原伤害值004110CC   .  E8 084A0100   call Ekd54.00425AD9              输入增益比例、原伤害值，从这里得到伤害的增益值存在eax中004110D1   .  0145 FC       add dword ptr ss:[ebp-4],eax      将增益值加到原伤害中004110D4   >  EB 5A         jmp short Ekd54.00411130         跳到411130，然后就结束子程序了。因为此时加强攻击和未击退敌人的突破攻击都完成了伤害增益的任务这里非常简单，就是要注意加强攻击和突破攻击都会进这部分。计算完伤害加成后就可以结束子程序了。第三部分：突破攻击是否造成后退第一部分提到如果攻击者有突破攻击，那么会跳到4110D6。现在就需要判断本次攻击能否造成后退。004110D6   >  8B45 0C       mov eax,dword ptr ss:[ebp+C]004110D9   .  66:8B48 06    mov cx,word ptr ds:[eax+6]004110DD   .  66:894D F0    mov word ptr ss:[ebp-10],cx004110E1   .  8B45 10       mov eax,dword ptr ss:[ebp+10]004110E4   .  FF70 06       push dword ptr ds:[eax+6]004110E7   .  FF75 F0       push dword ptr ss:[ebp-10]004110EA   .  E8 D1000000   call Ekd54.004111C0004110EF   .  0045 F0       add byte ptr ss:[ebp-10],al004110F2   .  0065 F1       add byte ptr ss:[ebp-F],ah004110F5   .  8D45 F0       lea eax,dword ptr ss:[ebp-10]004110F8   .  50            push eax004110F9   .  E8 9AB20200   call Ekd54.0043C398004110FE   .  85C0          test eax,eax00411100   .  74 20         je short Ekd54.0041112200411102   .  8D45 F0       lea eax,dword ptr ss:[ebp-10]00411105   .  50            push eax00411106   .  E8 79470200   call Ekd54.004358840041110B  |.  83C4 04       add esp,40041110E  |.  3C FF         cmp al,0FF                         检测是否造成后退，al=FF表示可以击退，al≠FF表示无法击退00411110   >  75 10         jnz short Ekd54.00411122   如果无法击退，跳转到411122这一大段都在分析能不能后退，具体分析是否后撤的过程都在那些子程序里，倒是没有分析它们的必要。第四部分：突破攻击的伤害计算和后撤动作阶段分离要注意的是，这个子程序其实在两个时刻都会被调用：一个是伤害计算的时候调用，另一个是攻击完成要响应敌人后撤动作的时候调用，现在这部分就是要判断现在处于那种时刻，并分离这两部分。由于接下来 能击退的代码和不能击退的代码交叉比较多，因此我接下来的注释会提前标注这里处理的是哪种情况的。00411112   .  FF75 0C       push dword ptr ss:[ebp+C]00411115   .  8D45 F0       lea eax,dword ptr ss:[ebp-10]00411118   .  50            push eax00411119   .  E8 62820400   call Ekd54.004593800041111E   .  3C FE         cmp al,0FE00411120   .  72 08         jb short Ekd54.0041112A         【可击退】可以击退的情况下，从这里跳转到41112A00411122   >  837D 08 01    cmp dword ptr ss:[ebp+8],1    【不可击退】不可击退的情况会跳转到这里。这里检测是否处于伤害计算阶段，[ebp+8]=1表示现在在响应攻击后撤动作，[ebp+8]=0表示现在在做伤害计算00411126   .^ 75 98         jnz short Ekd54.004110C0       【不可击退】如果是在做伤害计算，则跳转回4110C0去计算40%的额外伤害，大家可以回到第二部分去看。如果是在做响应后撤动作，那么直接从下面那句跳出子程序了。因为此时是不可击退的情况，不需要做后撤动作。00411128   .  EB 09         jmp short Ekd54.004111330041112A   >  837D 08 00    cmp dword ptr ss:[ebp+8],0  【可击退】可击退的情况会跳转到这里，这里检测是否处于伤害计算阶段，[ebp+8]=1表示现在在响应后撤动作；[ebp+8]=0表示现在在做伤害计算0041112E   .  75 05         jnz short Ekd54.00411135        【可击退】如果是在响应后撤动作，则跳转到411135继续响应动作；如果是在计算伤害，直接从411133那跳出结束，因为可击退的情况下不需要额外做伤害计算。00411130   >  8B55 FC       mov edx,dword ptr ss:[ebp-4]00411133   >  EB 77         jmp short Ekd54.004111AC这里就是四种情况：1、可击退-计算伤害（其实不计算，等于直接结束）2、可击退-执行击退动作3、不可击退-计算伤害4、不可击退-执行击退动作（其实不执行，等于直接结束）捋清楚这几个逻辑是怎么跳转分流的，基本这个特技就搞清楚了。第五部分：击退动作响应三个条件：1、拥有突破攻击特技；2、敌人可以被击退；3、处于击退动作响应阶段而非伤害计算阶段。满足这三个条件就可以进入到这部分，就是一些很简单的显示文字和后撤、转向动作的执行了。00411135   >  8B4D 0C       mov ecx,dword ptr ss:[ebp+C]00411138   .  E8 33E50400   call Ekd54.0045F6700041113D   .  8945 EC       mov dword ptr ss:[ebp-14],eax00411140   .  50            push eax              这里是push被攻击者的data编号00411141   .  68 FF0C5000   push Ekd54.00500CFF         这里是push“唔，好强的xx”文字的内存地址00411146   .  E8 12850400   call Ekd54.0045965D           这个子程序能够完成被攻击者说话。0041114B   .  8B4D F8       mov ecx,dword ptr ss:[ebp-8]0041114E   .  8B01          mov eax,dword ptr ds:[ecx]00411150   .  8945 E8       mov dword ptr ss:[ebp-18],eax00411153   .  C605 7FE74C00>mov byte ptr ds:[4CE77F],10041115A   .  68 FFFF0000   push 0FFFF0041115F   .  FF75 F1       push dword ptr ss:[ebp-F]        这个-F很迷惑00411162   .  FF75 F0       push dword ptr ss:[ebp-10]00411165   .  FF75 EC       push dword ptr ss:[ebp-14]      这里是push被攻击者的data编号00411168   .  E8 70830400   call Ekd54.004594DD            被攻击者完成后撤动作0041116D   .  C605 7FE74C00>mov byte ptr ds:[4CE77F],000411174   .  8B4D 10       mov ecx,dword ptr ss:[ebp+10]00411177   .  FF31          push dword ptr ds:[ecx]00411179   .  8B4D 0C       mov ecx,dword ptr ss:[ebp+C]0041117C   .  FF31          push dword ptr ds:[ecx]0041117E   .  E8 84D70000   call Ekd54.0041E907            被攻击者朝向转回来。再下面的几句代码不解读了，都是和主线工作关系不密切的内容了。00411183   .  8B4D F8       mov ecx,dword ptr ss:[ebp-8]00411186   .  8B45 E8       mov eax,dword ptr ss:[ebp-18]00411189   .  8901          mov dword ptr ds:[ecx],eax0041118B   .  A0 00284900   mov al,byte ptr ds:[492800]00411190   .  A2 282C4B00   mov byte ptr ds:[4B2C28],al00411195   .  50            push eax00411196   .  6A 00         push 000411198   .  6A 00         push 00041119A   .  6A 50         push 500041119C   .  6A 02         push 20041119E   .  8B4D 10       mov ecx,dword ptr ss:[ebp+10]004111A1   .  E8 D2A60000   call Ekd54.0041B878004111A6   .  5A            pop edx004111A7   .  E8 9AFE0500   call Ekd54.00471046004111AC   >  8BE5          mov esp,ebp004111AE   .  5D            pop ebp004111AF   .  C2 0C00       retn 0C代码解读就到这里了，不得不说star大神们的代码结构相当紧凑，用最简短的代码完成了最复杂的功能。现在我们拿到了加强攻击突破攻击的分离位置、显示对话的位置、后撤转向的位置、突破攻击是否击退的判断代码、击退和不击退以后在哪里做什么处理的逻辑，就可以介入去修改一些东西了。
特技修改一、对话修改在一楼我们分析过，对话的逻辑在：00411140   .  50            push eax00411141   .  68 FF0C5000   push Ekd54.00500CFF00411146   .  E8 12850400   call Ekd54.0045965D如果不需要对话的话，把这几行代码直接给nop掉就可以了，当然有个更快的办法就是把500CFF这4个字节变成0，因为对话框如果检测到对话内容一开始就是0（也就是结束符），那么就根本不会弹出，这样也能达到效果。如果需要修改成自己想要的对话的话，我们可以关注一下500CFF地址：
这里要注意，在od中是从右往左读的（因为小端存储），所以从500CFF中按顺序读出来的字节是：DF ED A3 AC BA C3 C7 BF……如果我们需要把击退后的对话改成自己的，可以去文字转gbk的网站中输入自己想要的对话，得到十六进制字节流，例如：
连续两个十六进制数为1个字节，但是内存区的地址顺序是从右向左的，所以别忘了反着输入：
这样就能得到最终的效果了：
二、限制地形不击退有时候我们希望在可恢复地形中的人不会被击退，这个修改zhoufangzun大佬发过一个6.2版本的，现在6.3突破攻击代码大改后已经不适用了，我正好也重新做了一下。思路很简单，在一楼中我们已经指出了：0041110E  |.  3C FF         cmp al,0FF                         检测是否造成后退，al=FF表示可以击退，al≠FF表示无法击退00411110   >  75 10         jnz short Ekd54.00411122   如果无法击退，跳转到411122这句话在判断可不可以被击退。因此我们可以从这里跳出，多加一个地形检测，如果地形是可恢复地形的话就强行把al赋值为0：0041110B   . /E9 02F50100   jmp Ekd54.00430612E9 02 F5 01 0000430612   > \83C4 04       add esp,400430615   .  50            push eax00430616   .  8B4D 0C       mov ecx,dword ptr ss:[ebp+C]00430619   .  E8 422DFDFF   call Ekd54.004033600043061E   .  50            push eax0043061F   .  E8 6D530000   call Ekd54.0043599100430624   .  3C 12         cmp al,1200430626   .  72 0C         jb short Ekd54.0043063400430628   .  3C 16         cmp al,160043062A   .  77 08         ja short Ekd54.004306340043062C   .  58            pop eax0043062D   .  B8 00000000   mov eax,000430632   .  EB 01         jmp short Ekd54.0043063500430634   >  58            pop eax00430635   >  3D FF000000   cmp eax,0FF0043063A   .^ E9 D10AFEFF   jmp Ekd54.0041111083 C4 04 50 8B 4D 0C E8 42 2D FD FF 50 E8 6D 53 00 00 3C 12 72 0C 3C 16 77 08 58 B8 00 00 00 00EB 01 58 3D FF 00 00 00 E9 D1 0A FE FF这样在可恢复地形上的武将就不会被击退了。

## 二、盾墙防突破版（补丁文本）

```text
突破攻击位置

CPU Disasm

地址        十六进制数据              汇编代码                               注释

0041110B  |. /E9 FEF40100     jmp 0043060E

CPU Disasm

地址        十六进制数据              汇编代码                               注释

0043060E  /> \83C4 04         add esp,4

00430611  |.  50              push eax

00430612  |.  8B4D 0C         mov ecx,dword ptr [ebp+0C]

00430615  |.  6A 00           push 0                             ; /Arg4 = 0

00430617  |.  6A 01           push 1                             ; |Arg3 = 1

00430619  |.  68 00000000     push 0                             ; |Arg2 = 0

0043061E  |.  68 77000000     push 77                            ; |Arg1 = 77

00430623  |.  E8 B1FBFDFF     call 004101D9                      ; \Ekd5盾墙防突破.004101D9

00430628  |.  85C0            test eax,eax

0043062A  |.  74 14           jz short 00430640

0043062C  |.  FF75 0C         push dword ptr [ebp+0C]            ; /Arg2 => [ARG.2]

0043062F  |.  FF75 10         push dword ptr [ebp+10]            ; |Arg1 => [ARG.3]

00430632  |.  E8 1E230A00     call 004D2955                      ; \Ekd5盾墙防突破.004D2955

00430637  |.  85C0            test eax,eax

00430639  |.  74 05           jz short 00430640

0043063B  |.  58              pop eax

0043063C  |.  31C0            xor eax,eax

0043063E  |.  EB 01           jmp short 00430641

00430640  |>  58              pop eax

00430641  |>  3D FF000000     cmp eax,0FF

00430646  \.^ E9 C50AFEFF     jmp 00411110

83 C4 04 50 8B 4D 0C 6A 00 6A 01 68 00 00 00 00

68 77 00 00 00 E8 B1 FB FD FF 85 C0 74 14 FF 75

0C FF 75 10 E8 1E 23 0A 00 85 C0 74 05 58 31 C0

EB 01 58 3D FF 00 00 00 E9 C5 0A FE FF

盾墙写法调整

CPU Disasm

地址        十六进制数据              汇编代码                               注释

004D292E  |. /74 1C           jz short 004D294C

004D2930  |. |50              push eax

004D2931  |. |FF75 0C         push dword ptr [ebp+0C]            ; /Arg2 => [Arg2]

004D2934  |. |FF75 08         push dword ptr [ebp+8]             ; |Arg1 => [Arg1]

004D2937  |. |E8 19000000     call 004D2955                      ; \Ekd5盾墙防突破.004D2955

004D293C  |. |5A              pop edx

004D293D  |. |0FAFC2          imul eax,edx

004D2940  |. |50              push eax                           ; /Arg2

004D2941  |. |FF75 10         push dword ptr [ebp+10]            ; |Arg1 => [Arg3]

004D2944  |. |E8 9031F5FF     call 00425AD9                      ; \Ekd5盾墙防突破.00425AD9

004D2949  |. |2945 10         sub dword ptr [ebp+10],eax

004D294C  |> \8B45 10         mov eax,dword ptr [ebp+10]

004D294F  |.  8BE5            mov esp,ebp

004D2951  |.  5D              pop ebp

004D2952  \.  C2 1000         retn 10

004D2955  /$  55              push ebp                           ; Ekd5盾墙防突破.004D2955(guessed Arg1,Arg2)

004D2956  |.  8BEC            mov ebp,esp

004D2958  |.  8B4D 08         mov ecx,dword ptr [ebp+8]

004D295B  |.  8079 0E 07      cmp byte ptr [ecx+0E],7

004D295F  |.  74 10           je short 004D2971

004D2961  |.  BA C2E84800     mov edx,0048E8C2

004D2966  |.  66:813A FFFF    cmp word ptr [edx],0FFFF

004D296B  |.  74 04           je short 004D2971

004D296D  |.  FF32            push dword ptr [edx]

004D296F  |.  EB 03           jmp short 004D2974

004D2971  |>  FF71 06         push dword ptr [ecx+6]

004D2974  |>  8B4D 0C         mov ecx,dword ptr [ebp+0C]

004D2977  |.  8A41 0F         mov al,byte ptr [ecx+0F]

004D297A  |.  8BD0            mov edx,eax

004D297C  |.  83E2 01         and edx,00000001

004D297F  |.  85D2            test edx,edx

004D2981  |.  75 16           jnz short 004D2999

004D2983  |.  8A51 07         mov dl,byte ptr [ecx+7]

004D2986  |.  3A55 FD         cmp dl,byte ptr [ebp-3]

004D2989  |.  74 26           je short 004D29B1

004D298B  |.  77 06           ja short 004D2993

004D298D  |.  3C 00           cmp al,0

004D298F  |.  74 24           je short 004D29B5

004D2991  |.  EB 1A           jmp short 004D29AD

004D2993  |>  3C 02           cmp al,2

004D2995  |.  74 1E           je short 004D29B5

004D2997  |.  EB 14           jmp short 004D29AD

004D2999  |>  8A51 06         mov dl,byte ptr [ecx+6]

004D299C  |.  3A55 FC         cmp dl,byte ptr [ebp-4]

004D299F  |.  74 10           je short 004D29B1

004D29A1  |.  77 06           ja short 004D29A9

004D29A3  |.  3C 01           cmp al,1

004D29A5  |.  74 06           je short 004D29AD

004D29A7  |.  EB 0C           jmp short 004D29B5

004D29A9  |>  3C 03           cmp al,3

004D29AB  |.  75 08           jne short 004D29B5

004D29AD  |>  B0 01           mov al,1

004D29AF  |.  EB 06           jmp short 004D29B7

004D29B1  |>  B0 00           mov al,0

004D29B3  |.  EB 02           jmp short 004D29B7

004D29B5  |>  B0 00           mov al,0

004D29B7  |>  8BE5            mov esp,ebp

004D29B9  |.  5D              pop ebp

004D29BA  \.  C2 0800         retn 8

74 1C 50 FF 75 0C FF 75 08 E8 19 00 00 00 5A 0F

AF C2 50 FF 75 10 E8 90 31 F5 FF 29 45 10 8B 45

10 8B E5 5D C2 10 00 55 8B EC 8B 4D 08 80 79 0E

07 74 10 BA C2 E8 48 00 66 81 3A FF FF 74 04 FF

32 EB 03 FF 71 06 8B 4D 0C 8A 41 0F 8B D0 83 E2

01 85 D2 75 16 8A 51 07 3A 55 FD 74 26 77 06 3C

00 74 24 EB 1A 3C 02 74 1E EB 14 8A 51 06 3A 55

FC 74 10 77 06 3C 01 74 06 EB 0C 3C 03 75 08 B0

01 EB 06 B0 00 EB 02 B0 00 8B E5 5D C2 08 00
```

## 三、偷袭攻击分析

```text
CPU Disasm
地址        十六进制数据              汇编代码                               注释
004D2700  /$  55              push ebp                           ; Ekd5盾墙.004D2700(guessed Arg1,Arg2,Arg3)
004D2701  |.  8BEC            mov ebp,esp
004D2703  |.  33C0            xor eax,eax
004D2705  |.  50              push eax
004D2706  |.  8B4D 08         mov ecx,dword ptr [ebp+8]
得出攻击方战场内存地址
004D2709  |.  8079 0E 07      cmp byte ptr [ecx+0E],7
Ecx+0e是判断是否可控，如果等于7则为可控单位，跳转到4D271F
004D270D  |.  74 10           je short 004D271F
004D270F  |.  BA C2E84800     mov edx,0048E8C2
004D2714  |.  66:813A FFFF    cmp word ptr [edx],0FFFF
004D2719  |.  74 04           je short 004D271F
004D271B  |.  FF32            push dword ptr [edx]
004D271D  |.  EB 03           jmp short 004D2722
004D271F  |>  FF71 06         push dword ptr [ecx+6]
ECX+6是攻击方的横坐标，dword是四字节，即+6、+7（纵坐标）、+8、+9，压栈保存
004D2722  |>  8B4D 0C         mov ecx,dword ptr [ebp+0C]
Ebp+0c存的是被攻击方的战场内存地址，存入ecx
004D2725  |.  8A41 0F         mov al,byte ptr [ecx+0F]
Ecx+0f是被攻击方的朝向，0上，1右，2下，3左，单字节存入eax（al）
004D2728  |.  8BD0            mov edx,eax
存到edx
004D272A  |.  83E2 01         and edx,00000001
判断edx是否为奇数，如果被攻击目标为上下朝向（即0或2），则运行结果为0，如果左右朝向运行结果为1
004D272D  |.  85D2            test edx,edx
判断上述运行结果是否为0
004D272F  |.  75 16           jnz short 004D2747
Jnz是不相同跳转，在这里是如果test的结果为1，即被攻击人物是左右朝向，则跳转到4D2747
004D2731  |.  8A51 07         mov dl,byte ptr [ecx+7]
上下朝向走这，ecx+7是被打的人的纵坐标
004D2734  |.  3A55 F9         cmp dl,byte ptr [ebp-7]
Ebp-7是epb-8+1，即攻击方的纵坐标，进行比较
004D2737  |.  74 26           je short 004D275F
如果纵坐标相等，说明是侧向增伤，跳转至4D275F
004D2739  |.  77 06           ja short 004D2741
如果dl更大，即被打的人在下面（上打下），那么跳到4D2741，否则往下走
004D273B  |.  3C 00           cmp al,0
0是朝上，下打上的情况下，判断被打的人朝向是否朝上
004D273D  |.  74 24           je short 004D2763
朝上就跳到4D2763，背面增伤，朝下就往下走
004D273F  |.  EB 1A           jmp short 004D275B
朝下就正面不增伤，跳到4D275B
004D2741  |>  3C 02           cmp al,2
2是朝下，判断被打的人朝向是否向下
004D2743  |.  74 1E           je short 004D2763
Je相同跳转，即如果向下就跳到4D2763，为上打下背面增伤，反之直接往下走
004D2745  |.  EB 14           jmp short 004D275B
跳到4D275B，正面不增伤
004D2747  |>  8A51 06         mov dl,byte ptr [ecx+6]
Ecx+6是被攻击人物的横坐标，byte是单字节存入edx(dl)
004D274A  |.  3A55 F8         cmp dl,byte ptr [ebp-8]
Ebp-8是上面入栈的攻击方人物的信息（战场内存地址+6，+7，+8，+9），byte即为+6，即攻击方的横坐标，将dl（被攻击人物的横坐标）与其相比较
004D274D  |.  74 10           je short 004D275F
Je是等于跳转，当攻击双方横坐标相等，被攻击方又是左右朝向，因此可以得出是侧面攻击，跳转至4D275F
004D274F  |.  77 06           ja short 004D2757
Ja是大于跳转，即如果被攻击方的横坐标更大（从左边打右边），则跳转到4D2757，否则继续往下走
004D2751  |.  3C 01           cmp al,1
Al还是之前的被攻击方朝向，1是朝右
004D2753  |.  74 06           je short 004D275B
相等判定，如果al是1，即朝向右边，那么就跳转到4D275B，又因为现在是右打左（左打右跳到下面去了），所以是正面，不加伤害
004D2755  |.  EB 0C           jmp short 004D2763
跳到4D2763
004D2757  |>  3C 03           cmp al,3
左打右的情况下，对比被打的人方向是不是朝左（3）
004D2759  |.  75 08           jne short 004D2763
如果是朝左就是正面不增伤，往下走（清零），反之背面增伤，跳转至4D2763
004D275B  |>  33C0            xor eax,eax
Eax清零，
004D275D  |.  EB 06           jmp short 004D2765
跳转至4D2765
004D275F  |>  B0 01           mov al,1
增伤倍率为1，即1*系数（背面是双倍，即2*系数）
004D2761  |.  EB 02           jmp short 004D2765
跳转至4D2765
004D2763  |>  B0 02           mov al,2
增伤倍率为2
004D2765  |>  6BC0 19         imul eax,eax,19
增伤系数是19H（即25），由于是侧面增伤因此是1*25=25，正面不增伤是0
004D2768  |.  50              push eax                           ; /Arg2
输入1：增伤系数
004D2769  |.  FF75 10         push dword ptr [ebp+10]            ; |Arg1 => [Arg3]
输入2：基础伤害
004D276C  |.  E8 6833F5FF     call 00425AD9                      ; \Ekd5盾墙.00425AD9
这段函数应该就是将两个输入简单相乘，输出结果存在eax
004D2771  |.  0145 10         add dword ptr [ebp+10],eax
给基础伤害加上增伤的数值
004D2774  |.  0145 FC         add dword ptr [ebp-4],eax
Ebp-4是最开始入栈的eax（0）
004D2777  |.  8B4D 0C         mov ecx,dword ptr [ebp+0C]
被攻击方战场内存地址
004D277A  |.  E8 913FF3FF     call 00406710
这段函数
004D277F  |.  3C 01           cmp al,1
004D2781  |.  74 19           je short 004D279C
004D2783  |.  803D 9A0E5000 0 cmp byte ptr [500E9A],1
004D278A  |.  75 10           jne short 004D279C
004D278C  |.  6A 19           push 19                            ; /Arg2 = 19
004D278E  |.  FF75 10         push dword ptr [ebp+10]            ; |Arg1 => [Arg3]
004D2791  |.  E8 4333F5FF     call 00425AD9                      ; \Ekd5盾墙.00425AD9
004D2796  |.  0145 10         add dword ptr [ebp+10],eax
004D2799  |.  0145 FC         add dword ptr [ebp-4],eax
004D279C  |>  8B45 10         mov eax,dword ptr [ebp+10]
004D279F  \.  EB 03           jmp short 004D27A4
004D27A1  /.  8B45 FC         mov eax,dword ptr [ebp-4]
004D27A4  |>  8BE5            mov esp,ebp
004D27A6  |.  5D              pop ebp
004D27A7  \.  C2 0C00         retn 0C
```