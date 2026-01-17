using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Enums;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Infrastructure.Services;

public class WorkItemService : IWorkItemService
{
    private readonly SynapseDbContext _context;

    public WorkItemService(SynapseDbContext context)
    {
        _context = context;
    }

    public async Task<WorkItem> CreateWorkItemAsync(WorkItem workItem)
    {
        // Generate code if not provided
        if (string.IsNullOrEmpty(workItem.Code))
        {
            workItem.Code = await GenerateWorkItemCodeAsync(workItem.ProjectId);
        }

        _context.WorkItems.Add(workItem);
        await _context.SaveChangesAsync();

        // Create history entry
        await CreateHistoryEntryAsync(workItem.Id, "Status", null, workItem.Status.ToString(), "Work item created");

        return workItem;
    }

    public async Task<WorkItem?> GetWorkItemByIdAsync(Guid id)
    {
        return await _context.WorkItems
            .Include(w => w.Project)
            .Include(w => w.Sprint)
            .Include(w => w.Component)
            .Include(w => w.Assignee)
            .Include(w => w.Reporter)
            .Include(w => w.Comments)
                .ThenInclude(c => c.Author)
            .Include(w => w.Checklists)
                .ThenInclude(c => c.Items)
            .Include(w => w.ChildWorkItems)
            .FirstOrDefaultAsync(w => w.Id == id);
    }

    public async Task<IEnumerable<WorkItem>> GetWorkItemsByProjectAsync(Guid projectId)
    {
        return await _context.WorkItems
            .Where(w => w.ProjectId == projectId)
            .Include(w => w.Assignee)
            .Include(w => w.Sprint)
            .Include(w => w.Component)
            .OrderByDescending(w => w.Priority)
            .ThenBy(w => w.OrderIndex)
            .ToListAsync();
    }

    public async Task<IEnumerable<WorkItem>> GetWorkItemsBySprintAsync(Guid sprintId)
    {
        return await _context.WorkItems
            .Where(w => w.SprintId == sprintId)
            .Include(w => w.Assignee)
            .Include(w => w.Component)
            .OrderBy(w => w.Status)
            .ThenByDescending(w => w.Priority)
            .ToListAsync();
    }

    public async Task<IEnumerable<WorkItem>> GetWorkItemsByAssigneeAsync(Guid userId)
    {
        return await _context.WorkItems
            .Where(w => w.AssigneeId == userId)
            .Include(w => w.Project)
            .Include(w => w.Sprint)
            .OrderByDescending(w => w.Priority)
            .ThenBy(w => w.DueDate)
            .ToListAsync();
    }

    public async Task UpdateWorkItemAsync(WorkItem workItem)
    {
        workItem.UpdatedAt = DateTime.UtcNow;
        _context.WorkItems.Update(workItem);
        await _context.SaveChangesAsync();
    }

    public async Task UpdateStatusAsync(Guid workItemId, WorkItemStatus newStatus)
    {
        var workItem = await _context.WorkItems.FindAsync(workItemId);
        if (workItem == null)
            throw new ArgumentException("Work item not found", nameof(workItemId));

        var oldStatus = workItem.Status;
        workItem.Status = newStatus;
        workItem.UpdatedAt = DateTime.UtcNow;

        // Set started/completed timestamps
        if (newStatus == WorkItemStatus.InProgress && !workItem.StartedAt.HasValue)
        {
            workItem.StartedAt = DateTime.UtcNow;
        }
        else if (newStatus == WorkItemStatus.Done && !workItem.CompletedAt.HasValue)
        {
            workItem.CompletedAt = DateTime.UtcNow;
            workItem.ProgressPercentage = 100;
        }

        await _context.SaveChangesAsync();

        // Create history entry
        await CreateHistoryEntryAsync(workItemId, "Status", oldStatus.ToString(), newStatus.ToString());
    }

    public async Task AssignWorkItemAsync(Guid workItemId, Guid? assigneeId)
    {
        var workItem = await _context.WorkItems.FindAsync(workItemId);
        if (workItem == null)
            throw new ArgumentException("Work item not found", nameof(workItemId));

        var oldAssigneeId = workItem.AssigneeId;
        workItem.AssigneeId = assigneeId;
        workItem.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();

        // Create history entry
        await CreateHistoryEntryAsync(workItemId, "Assignee",
            oldAssigneeId?.ToString(), assigneeId?.ToString());
    }

    public async Task<string> GenerateWorkItemCodeAsync(Guid projectId)
    {
        var project = await _context.Projects.FindAsync(projectId);
        if (project == null)
            throw new ArgumentException("Project not found", nameof(projectId));

        var count = await _context.WorkItems.CountAsync(w => w.ProjectId == projectId);
        return $"{project.Code}-{count + 1}";
    }

    private async Task CreateHistoryEntryAsync(
        Guid workItemId,
        string fieldName,
        string? oldValue,
        string? newValue,
        string? summary = null)
    {
        var history = new WorkItemHistory
        {
            WorkItemId = workItemId,
            FieldName = fieldName,
            OldValue = oldValue,
            NewValue = newValue,
            ChangeSummary = summary ?? $"{fieldName} changed from '{oldValue}' to '{newValue}'"
        };

        _context.WorkItemHistories.Add(history);
        await _context.SaveChangesAsync();
    }
}
