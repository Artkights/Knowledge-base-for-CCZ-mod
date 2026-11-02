using System.Data;
using System.Reflection;
using DataManager.App;
using DataManager.Core.Domain;

namespace DataManager.Tests;

internal static class RecordQueryUiTests
{
    public static void Run(string source)
    {
        var copy = TestSupport.CreateCoreCopy(source);
        using var form = new MainForm(false) { StartPosition = FormStartPosition.Manual,
            Location = new Point(-32000, -32000), ShowInTaskbar = false, Size = new Size(1280, 720) };
        try
        {
            form.Show(); form.LoadProjectForSmokeTest(copy); Application.DoEvents();
            var workspace = form.WorkspaceForSmokeTest;
            var persons = workspace.GetDocument("persons");
            var id = Convert.ToInt32(persons.Data.Rows[42]["ID"]);
            new BusinessDataService(workspace).BeginTransaction(BusinessPageKind.Persons)
                .SetById("persons", id, "名称", "查'[]*验").Apply();
            TestSupport.Assert(form.QueryForSmokeTest("'[]*"), "字面关键词查询失败");
            TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == 1 && SelectedId(form) == id,
                "姓名特殊字符没有按字面匹配，或选择使用了筛选下标");
            TestSupport.Assert(form.BusinessEditorForSmokeTest.CurrentId == id, "查询没有绑定真实人物ID");
            TestSupport.Assert(form.QuerySummaryForSmokeTest.Contains("匹配 1 /"), "没有查询结果数量");
            CheckLabelOnlyQueryAndCandidates(form, id);
            TestSupport.Assert(form.QueryForSmokeTest("'[]*"), "候选验证后不能恢复姓名查询");
            form.SelectModuleForSmokeTest("策略");
            TestSupport.Assert(form.QueryForSmokeTest("__没有匹配的测试内容__") && form.EmptyQueryForSmokeTest && form.EntityListForSmokeTest.Items.Count == 0,
                "零结果没有显示空详情状态");
            form.SelectModuleForSmokeTest("人物");
            TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == 1 && SelectedId(form) == id, "返回页面丢失独立查询状态");
            form.QuickLocateForSmokeTest(id + 1);
            TestSupport.Assert(form.BusinessEditorForSmokeTest.CurrentId == id + 1 && form.EntityListForSmokeTest.Items.Count == persons.Data.Rows.Count,
                "快速定位没有清除筛选并跳到筛选外记录");

            // Typed input must be accepted into the draft before the search snapshot is rebuilt.
            form.QuickLocateForSmokeTest(id);
            var editors = Descendants(form.BusinessEditorForSmokeTest).OfType<ByteTextEditor>().ToArray();
            var nameEditor = editors.Single(editor => editor.Editor.Text == "查'[]*验");
            nameEditor.Editor.Focus(); nameEditor.Editor.Text = "未失焦查询";
            TestSupport.Assert(form.QueryForSmokeTest("未失焦查询") && SelectedId(form) == id && Convert.ToString(persons.Data.Rows[42]["名称"]) == "未失焦查询",
                "查询丢失未失焦输入或读取了提交前的名称");
            form.UndoDraftForSmokeTest(); Application.DoEvents();
            TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == 0 && form.EmptyQueryForSmokeTest, "撤回后没有重新计算查询");
            form.QueryForSmokeTest(string.Empty);

            // Physical tables and the left navigation use the same matching IDs.
            form.ShowPhysicalTableForSmokeTest("persons");
            TestSupport.Assert(form.QueryForSmokeTest("'[]*"), "物理表查询失败");
            var grid = form.PhysicalGridForSmokeTest;
            TestSupport.Assert(grid.RowCount == 1 && (int)((DataRowView)grid.Rows[0].DataBoundItem)["ID"] == id && SelectedId(form) == id,
                "物理表筛选或导航的真实ID不一致");
            var detailsOnly = "仅详情唯一词";
            TestSupport.Assert(form.QueryForSmokeTest(detailsOnly) && grid.RowCount == 0 && form.EntityListForSmokeTest.Items.Count == 0,
                "物理人物表查询错误匹配仅存在于列传详情的关键词");
            TestSupport.Assert(form.QueryForSmokeTest("60001") && grid.RowCount == 0 && form.EntityListForSmokeTest.Items.Count == 0,
                "物理人物表查询错误匹配仅存在于初始HP的数字");
            TestSupport.Assert(form.QueryForSmokeTest("'[]*"), "详情字段排除检查后姓名查询失败");
            CheckPhysicalCandidateSelection(form, id);
            TestSupport.Assert(form.QueryForSmokeTest("'[]*"), "候选定位检查后姓名查询失败");
            var before = persons.Data.Rows[42]["武力"];
            grid.CurrentCell = grid.Rows[0].Cells["武力"];
            grid.BeginEdit(true); ((TextBox)grid.EditingControl!).Text = Convert.ToInt32(before) == 99 ? "98" : "99";
            TestSupport.Assert(form.QueryForSmokeTest(string.Empty), "当前表格编辑阻止正常查询");
            TestSupport.Assert(Convert.ToInt32(persons.Data.Rows[42]["武力"]) != Convert.ToInt32(before), "筛选后编辑没有提交真实源行");
            TestSupport.Assert(Convert.ToInt32(persons.Data.Rows[0]["ID"]) != id, "测试基底ID不满足隔离条件");

            form.QuickLocateForSmokeTest(id + 1);
            TestSupport.Assert(SelectedId(form) == id + 1 && (int)((DataRowView)grid.CurrentRow!.DataBoundItem)["ID"] == id + 1,
                "物理表快速定位没有同步左侧真实ID");
            var invalidRow = grid.CurrentRow!;
            grid.CurrentCell = invalidRow.Cells["武力"]; grid.BeginEdit(true);
            ((TextBox)grid.EditingControl!).Text = "9999999";
            var previousSummary = form.QuerySummaryForSmokeTest;
            var invalidQueryAccepted = form.QueryForSmokeTest("无效查询不得应用");
            TestSupport.Assert(!invalidQueryAccepted && form.QuerySummaryForSmokeTest == previousSummary && grid.IsCurrentCellInEditMode,
                $"无效输入被查询提交或丢失；accepted={invalidQueryAccepted} previous-summary=[{previousSummary}] summary=[{form.QuerySummaryForSmokeTest}] edit={grid.IsCurrentCellInEditMode} editor=[{grid.EditingControl?.Text}] status=[{form.StatusForSmokeTest}]");
            var hideEmpty = (CheckBox)typeof(MainForm).GetField("_hideEmpty", BindingFlags.Instance | BindingFlags.NonPublic)!.GetValue(form)!;
            hideEmpty.Checked = true;
            TestSupport.Assert(!hideEmpty.Checked && grid.IsCurrentCellInEditMode, "无效输入后隐藏空白行没有恢复勾选状态");
            grid.CancelEdit();
            form.QueryForSmokeTest("'[]*");
            grid.CurrentCell = grid.Rows[0].Cells["名称"];
            typeof(MainForm).GetMethod("GridKeyDown", BindingFlags.Instance | BindingFlags.NonPublic)!.Invoke(form, [grid, new KeyEventArgs(Keys.Delete)]);
            Application.DoEvents();
            TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == 0 && form.EmptyQueryForSmokeTest,
                "清空字段后没有更新查询结果");
            form.UndoDraftForSmokeTest();
            TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == 1 && SelectedId(form) == id, "撤回清空字段没有恢复查询记录");
            form.QueryForSmokeTest(string.Empty);

            var checkedTables = 0;
            foreach (var module in workspace.Modules)
            {
                form.SelectModuleForSmokeTest(module.Key);
                foreach (var key in module.TableKeys.Where(workspace.Documents.ContainsKey).Where(key => key is not "person-r-assign" and not "person-s-assign"))
                {
                    form.ShowPhysicalTableForSmokeTest(key);
                    form.QueryForSmokeTest(string.Empty);
                    var records = new RecordPresentationService(workspace).GetTableRecords(workspace.GetDocument(key));
                    TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == records.Count, key + "导航记录数错误");
                    if (records.Count > 0)
                    {
                        TestSupport.Assert(form.EntityListForSmokeTest.Items[0].ToString()!.StartsWith(records[0].Id + "："), key + "首ID错误");
                        TestSupport.Assert(form.EntityListForSmokeTest.Items[form.EntityListForSmokeTest.Items.Count - 1].ToString()!.StartsWith(records[^1].Id + "："), key + "尾ID错误");
                    }
                    checkedTables++;
                }
            }
            foreach (var size in new[] { new Size(1280, 720), new Size(1500, 900), new Size(1920, 1080) })
            {
                form.Size = size; Application.DoEvents();
                foreach (var control in Descendants(form).Where(control => control.Visible && control.Name is "RecordQuery" or "ExecuteQuery" or "ClearQuery"))
                    TestSupport.Assert(control.Parent!.ClientRectangle.Contains(control.Bounds), "查询控件被裁切：" + control.Name);
            }
            Console.WriteLine($"RECORD_QUERY_UI_TESTS_OK tables={checkedTables} label-only/details-excluded/candidates/literal-label-enter/explicit-selection/keyboard-selection/numeric-enter/numeric-button/dropdown-reopen/clear/literal/draft/empty/page-state/quick-locate/physical-ID/layout");
        }
        finally
        {
            // Dispose avoids a product save prompt; every edit belongs to the disposable fixture.
            form.Dispose(); Directory.Delete(copy, true);
        }
    }

    private static int SelectedId(MainForm form) => Convert.ToInt32(form.EntityListForSmokeTest.SelectedItem!.GetType().GetProperty("Id")!.GetValue(form.EntityListForSmokeTest.SelectedItem));

    private static SearchableIdComboBox QueryCombo(MainForm form)
        => (SearchableIdComboBox)typeof(MainForm).GetField("_queryText", BindingFlags.Instance | BindingFlags.NonPublic)!.GetValue(form)!;

    private static void TypeCandidateQuery(SearchableIdComboBox combo, string text)
    {
        combo.Focus();
        combo.Text = text;
        typeof(SearchableIdComboBox).GetMethod("OnTextUpdate", BindingFlags.Instance | BindingFlags.NonPublic)!.Invoke(combo, [EventArgs.Empty]);
        Application.DoEvents();
    }

    private static void CommitCandidate(SearchableIdComboBox combo, int id)
    {
        combo.SelectedItem = combo.Items.Cast<DataManager.App.IdNameOption>().Single(option => option.Id == id);
        typeof(SearchableIdComboBox).GetMethod("OnSelectionChangeCommitted", BindingFlags.Instance | BindingFlags.NonPublic)!.Invoke(combo, [EventArgs.Empty]);
        Application.DoEvents();
    }

    private static void PressQueryEnter(SearchableIdComboBox combo)
    {
        typeof(SearchableIdComboBox).GetMethod("OnKeyDown", BindingFlags.Instance | BindingFlags.NonPublic)!.Invoke(combo, [new KeyEventArgs(Keys.Enter)]);
        Application.DoEvents();
    }

    private static void ClearQuery(MainForm form)
    {
        var button = (Button)typeof(MainForm).GetField("_clearQueryButton", BindingFlags.Instance | BindingFlags.NonPublic)!.GetValue(form)!;
        button.PerformClick(); Application.DoEvents();
    }

    private static void ClickQuery(MainForm form)
    {
        var button = (Button)typeof(MainForm).GetField("_queryButton", BindingFlags.Instance | BindingFlags.NonPublic)!.GetValue(form)!;
        button.PerformClick(); Application.DoEvents();
    }

    private static void AssertVisibleQueryIds(MainForm form, IEnumerable<int> expected, string message)
    {
        var expectedIds = expected.Order().ToArray();
        var actualIds = form.EntityListForSmokeTest.Items.Cast<object>()
            .Select(item => Convert.ToInt32(item.GetType().GetProperty("Id")!.GetValue(item))).Order().ToArray();
        var combo = QueryCombo(form);
        TestSupport.Assert(actualIds.SequenceEqual(expectedIds),
            $"{message}；expected=[{string.Join(',', expectedIds)}] actual=[{string.Join(',', actualIds)}] text=[{combo.Text}] selected=[{combo.SelectedItem}] summary=[{form.QuerySummaryForSmokeTest}]");
    }

    private static void CheckLabelOnlyQueryAndCandidates(MainForm form, int id)
    {
        var workspace = form.WorkspaceForSmokeTest;
        var persons = workspace.GetDocument("persons");
        var biography = workspace.GetDocument("person-biography");
        var textField = biography.Definition.Fields.First(field => field.Kind == DataManager.Core.Models.FieldKind.FixedString);
        var targetName = Convert.ToString(persons.Data.Rows.Cast<DataRow>().Single(row => Convert.ToInt32(row["ID"]) == id)["名称"])!;
        var idSuffixCollision = persons.Data.Rows.Cast<DataRow>().Select(row => Convert.ToInt32(row["ID"]))
            .First(candidate => candidate != id && candidate.ToString().EndsWith(id.ToString(), StringComparison.Ordinal));
        new BusinessDataService(workspace).BeginTransaction(BusinessPageKind.Persons)
            .SetById("person-biography", id, textField.Name, "仅详情唯一词")
            .SetById("persons", id, "初始HP", 60001).Apply();
        new BusinessDataService(workspace).BeginTransaction(BusinessPageKind.Persons)
            .SetById("persons", idSuffixCollision, "名称", targetName).Apply();
        Application.DoEvents();
        var combo = QueryCombo(form);
        TestSupport.Assert(combo.DropDownStyle == ComboBoxStyle.DropDown, "查询框不能输入并展示下拉候选");
        TestSupport.Assert(form.QueryForSmokeTest("仅详情唯一词") && form.EntityListForSmokeTest.Items.Count == 0 && form.EmptyQueryForSmokeTest,
            "人物查询仍匹配列传详情而非左侧ID名称标签");
        TestSupport.Assert(form.QueryForSmokeTest("60001") && form.EntityListForSmokeTest.Items.Count == 0,
            "人物查询错误匹配仅存在于初始HP的数字");
        ClearQuery(form);
        TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == persons.Data.Rows.Count && combo.Text.Length == 0 && !form.EmptyQueryForSmokeTest,
            "清空按钮没有清除查询并恢复当前页全部记录");
        var selectedBefore = SelectedId(form);
        var countBefore = form.EntityListForSmokeTest.Items.Count;
        TypeCandidateQuery(combo, "仅详情唯一词");
        TestSupport.Assert(combo.Items.Count == 0, "实时下拉候选错误匹配人物详情字段");
        TypeCandidateQuery(combo, "60001");
        TestSupport.Assert(combo.Items.Count == 0, "实时下拉候选错误匹配初始HP数值");
        TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == countBefore && SelectedId(form) == selectedBefore,
            "编辑查询候选时提前改变了已执行的左侧筛选或选择");
        TypeCandidateQuery(combo, "'[]*");
        TestSupport.Assert(combo.Items.Count == 2 && combo.Items.Cast<DataManager.App.IdNameOption>().Select(option => option.Id).Order()
            .SequenceEqual(new[] { id, idSuffixCollision }.Order()),
            "姓名下拉候选未按左侧标签进行字面包含匹配");
        TypeCandidateQuery(combo, id + "：" + targetName);
        TestSupport.Assert(combo.Items.Cast<DataManager.App.IdNameOption>().Select(option => option.Id).Order()
            .SequenceEqual(new[] { id, idSuffixCollision }.Order()), "查询候选没有按左侧完整ID：名称标签匹配");
        PressQueryEnter(combo);
        AssertVisibleQueryIds(form, [id, idSuffixCollision], "完整标签纯输入后回车被错误当成精确候选选择");

        ClearQuery(form);
        TypeCandidateQuery(combo, "'[]*");
        combo.DroppedDown = false;
        Application.DoEvents();
        combo.DroppedDown = true;
        // A native keyboard selection changes the edit text before Enter. Do not
        // pump the posted popup restoration until the explicit selection commits.
        combo.SelectedItem = combo.Items.Cast<DataManager.App.IdNameOption>().Single(option => option.Id == idSuffixCollision);
        PressQueryEnter(combo);
        AssertVisibleQueryIds(form, [idSuffixCollision], "键盘改变候选后回车没有精确筛选实际ID，或被迟到的开窗恢复覆盖");
        TestSupport.Assert(form.BusinessEditorForSmokeTest.CurrentId == idSuffixCollision,
            "键盘选择查询候选后详情绑定了错误ID");

        ClearQuery(form);
        TypeCandidateQuery(combo, "'[]*");
        CommitCandidate(combo, id);
        TestSupport.Assert(SelectedId(form) == id && form.BusinessEditorForSmokeTest.CurrentId == id && form.EntityListForSmokeTest.Items.Count == 1,
            "选择姓名候选没有精确筛选并绑定实际人物ID");
        form.UndoDraftForSmokeTest(); Application.DoEvents();
        TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == 1 && SelectedId(form) == id, "撤回候选测试数据时丢失已选实际ID");
        ClearQuery(form);
        TypeCandidateQuery(combo, id.ToString());
        var expectedIds = combo.Options.Where(option => option.Display.Contains(id.ToString(), StringComparison.OrdinalIgnoreCase))
            .Select(option => option.Id).Order().ToArray();
        var candidateIds = combo.Items.Cast<DataManager.App.IdNameOption>().Select(option => option.Id).Order().ToArray();
        TestSupport.Assert(candidateIds.SequenceEqual(expectedIds) && candidateIds.Contains(id), "数字候选未按ID字符或左侧名称过滤");
        PressQueryEnter(combo);
        AssertVisibleQueryIds(form, expectedIds, "数字回车未执行与左侧ID名称相同范围的关键词查询");

        ClearQuery(form);
        TypeCandidateQuery(combo, id.ToString());
        ClickQuery(form);
        AssertVisibleQueryIds(form, expectedIds, "数字查询按钮错误精确选中了首个候选");

        ClearQuery(form);
        var allIds = form.EntityListForSmokeTest.Items.Cast<object>()
            .Select(item => Convert.ToInt32(item.GetType().GetProperty("Id")!.GetValue(item))).ToArray();
        TypeCandidateQuery(combo, id.ToString());
        combo.DroppedDown = false;
        Application.DoEvents();
        combo.DroppedDown = true;
        Application.DoEvents();
        var reopenedIds = combo.Items.Cast<DataManager.App.IdNameOption>().Select(option => option.Id).Order().ToArray();
        TestSupport.Assert(combo.Text == id.ToString() && reopenedIds.SequenceEqual(expectedIds),
            $"下拉收起后重新展开改变了数字输入或候选；expected-text=[{id}] actual-text=[{combo.Text}] expected=[{string.Join(',', expectedIds)}] actual=[{string.Join(',', reopenedIds)}]");
        AssertVisibleQueryIds(form, allIds, "重新展开候选提前改变了尚未执行的左侧查询");
        PressQueryEnter(combo);
        AssertVisibleQueryIds(form, expectedIds, "下拉收起再展开后回车错误精确选中了首个候选");
        ClearQuery(form);
    }

    private static void CheckPhysicalCandidateSelection(MainForm form, int id)
    {
        ClearQuery(form);
        var combo = QueryCombo(form);
        TypeCandidateQuery(combo, "'[]*");
        CommitCandidate(combo, id);
        var grid = form.PhysicalGridForSmokeTest;
        TestSupport.Assert(form.EntityListForSmokeTest.Items.Count == 1 && SelectedId(form) == id && grid.RowCount == 1 &&
            Convert.ToInt32(((DataRowView)grid.CurrentRow!.DataBoundItem)["ID"]) == id,
            "物理表候选选择使用了下拉序号或筛选后的行号");
    }

    private static IEnumerable<Control> Descendants(Control root)
    {
        foreach (Control child in root.Controls)
        { yield return child; foreach (var descendant in Descendants(child)) yield return descendant; }
    }
}
