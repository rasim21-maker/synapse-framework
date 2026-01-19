using SynapsePlatform.Core.Entities;

namespace SynapsePlatform.Core.Interfaces;

public interface IIDIService
{
    double CalculateComponentIDI(Component component);
    double CalculateProjectIDI(Guid projectId);
    Task<IDIReport> GetIDIReportAsync(Guid projectId);
    Task UpdateComponentIDIAsync(Guid componentId);
    Task<IEnumerable<Component>> GetComponentsNeedingIntegrationAsync(Guid projectId);
}

public interface ISprintService
{
    Task<Sprint> CreateSprintAsync(Sprint sprint);
    Task<Sprint?> GetActiveSprintAsync(Guid projectId);
    Task<IEnumerable<Sprint>> GetSprintsByProjectAsync(Guid projectId);
    Task StartSprintAsync(Guid sprintId);
    Task CompleteSprintAsync(Guid sprintId, string? whatWentWell, string? whatToImprove);
    Task<SprintMetrics> GetSprintMetricsAsync(Guid sprintId);
}

public interface IProjectService
{
    Task<Project> CreateProjectAsync(Project project);
    Task<Project?> GetProjectWithDetailsAsync(Guid id);
    Task<IEnumerable<Project>> GetProjectsByPortfolioAsync(Guid portfolioId);
    Task UpdateProjectPhaseAsync(Guid projectId, Core.Enums.ProjectPhase newPhase);
    Task<ProjectDashboard> GetProjectDashboardAsync(Guid projectId);
}

public interface IWorkItemService
{
    Task<WorkItem> CreateWorkItemAsync(WorkItem workItem);
    Task<WorkItem?> GetWorkItemWithDetailsAsync(Guid id);
    Task<IEnumerable<WorkItem>> GetBacklogAsync(Guid projectId);
    Task<IEnumerable<WorkItem>> GetSprintBacklogAsync(Guid sprintId);
    Task MoveToSprintAsync(Guid workItemId, Guid sprintId);
    Task UpdateStatusAsync(Guid workItemId, Core.Enums.WorkItemStatus status);
}

public class IDIReport
{
    public double ProjectIDI { get; set; }
    public Core.Enums.IDIStatus Status { get; set; }
    public IEnumerable<ComponentIDIInfo> Components { get; set; } = new List<ComponentIDIInfo>();
    public IEnumerable<IDITrend> Trends { get; set; } = new List<IDITrend>();
}

public class ComponentIDIInfo
{
    public Guid ComponentId { get; set; }
    public string ComponentName { get; set; } = string.Empty;
    public double IDI { get; set; }
    public Core.Enums.IDIStatus Status { get; set; }
    public int DaysSinceLastIntegration { get; set; }
}

public class IDITrend
{
    public DateTime Date { get; set; }
    public double IDI { get; set; }
}

public class ProjectDashboard
{
    public Project Project { get; set; } = null!;
    public Sprint? ActiveSprint { get; set; }
    public SprintMetrics? SprintMetrics { get; set; }
    public IDIReport IDIReport { get; set; } = null!;
    public int OpenWorkItems { get; set; }
    public int CompletedWorkItems { get; set; }
    public int BlockedWorkItems { get; set; }
    public int OpenRisks { get; set; }
    public double BudgetUtilization { get; set; }
}
