using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Enums;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Infrastructure.Services;

public class ProjectService : IProjectService
{
    private readonly SynapseDbContext _context;
    private readonly IIDIService _idiService;

    public ProjectService(SynapseDbContext context, IIDIService idiService)
    {
        _context = context;
        _idiService = idiService;
    }

    public async Task<Project> CreateProjectAsync(Project project)
    {
        // Generate code if not provided
        if (string.IsNullOrEmpty(project.Code))
        {
            var portfolio = await _context.Portfolios.FindAsync(project.PortfolioId);
            var count = await _context.Projects.CountAsync(p => p.PortfolioId == project.PortfolioId);
            project.Code = $"{portfolio?.Code ?? "PRJ"}-{count + 1:D3}";
        }

        _context.Projects.Add(project);
        await _context.SaveChangesAsync();
        return project;
    }

    public async Task<Project?> GetProjectByIdAsync(Guid id)
    {
        return await _context.Projects
            .Include(p => p.Portfolio)
            .Include(p => p.Components)
            .Include(p => p.Sprints)
            .Include(p => p.ProjectManager)
            .Include(p => p.TechLead)
            .FirstOrDefaultAsync(p => p.Id == id);
    }

    public async Task<Project?> GetProjectByCodeAsync(string code)
    {
        return await _context.Projects
            .Include(p => p.Portfolio)
            .Include(p => p.Components)
            .FirstOrDefaultAsync(p => p.Code == code);
    }

    public async Task<IEnumerable<Project>> GetProjectsByPortfolioAsync(Guid portfolioId)
    {
        return await _context.Projects
            .Where(p => p.PortfolioId == portfolioId)
            .Include(p => p.ProjectManager)
            .OrderBy(p => p.Name)
            .ToListAsync();
    }

    public async Task UpdateProjectAsync(Project project)
    {
        project.UpdatedAt = DateTime.UtcNow;
        _context.Projects.Update(project);
        await _context.SaveChangesAsync();
    }

    public async Task<ProjectDashboard> GetProjectDashboardAsync(Guid projectId)
    {
        var project = await _context.Projects
            .Include(p => p.Components)
            .Include(p => p.WorkItems)
            .Include(p => p.Sprints)
            .Include(p => p.Risks)
            .Include(p => p.QualityGates)
            .FirstOrDefaultAsync(p => p.Id == projectId);

        if (project == null)
            throw new ArgumentException("Project not found", nameof(projectId));

        var currentIDI = _idiService.CalculateProjectIDI(project);
        var activeSprint = project.Sprints.FirstOrDefault(s => s.IsActive);

        return new ProjectDashboard
        {
            Project = project,
            CurrentIDI = currentIDI,
            IDIStatus = _idiService.GetHealthStatus(currentIDI),
            TotalWorkItems = project.WorkItems.Count,
            CompletedWorkItems = project.WorkItems.Count(w => w.Status == WorkItemStatus.Done),
            BlockedWorkItems = project.WorkItems.Count(w => w.Status == WorkItemStatus.Blocked),
            OverdueWorkItems = project.WorkItems.Count(w =>
                w.DueDate.HasValue && w.DueDate < DateTime.UtcNow && w.Status != WorkItemStatus.Done),
            ActiveRisks = project.Risks.Count(r =>
                r.Status != RiskStatus.Closed && r.Status != RiskStatus.Occurred),
            FailedQualityGates = project.QualityGates.Count(g =>
                g.IsEnabled && g.LastCheckPassed == false),
            ActiveSprint = activeSprint,
            BudgetUtilization = project.PlannedBudget.HasValue && project.PlannedBudget > 0
                ? (double)((project.ActualBudget ?? 0) / project.PlannedBudget.Value * 100)
                : 0,
            DaysRemaining = project.PlannedEndDate.HasValue
                ? Math.Max(0, (project.PlannedEndDate.Value - DateTime.UtcNow).Days)
                : 0
        };
    }

    public async Task AdvancePhaseAsync(Guid projectId, ProjectPhase newPhase)
    {
        var project = await _context.Projects.FindAsync(projectId);
        if (project == null)
            throw new ArgumentException("Project not found", nameof(projectId));

        project.CurrentPhase = newPhase;
        project.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();
    }
}
