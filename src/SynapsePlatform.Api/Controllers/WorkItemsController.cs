using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Api.DTOs;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class WorkItemsController : ControllerBase
{
    private readonly SynapseDbContext _context;

    public WorkItemsController(SynapseDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<WorkItemDto>>> GetWorkItems(
        [FromQuery] Guid? projectId,
        [FromQuery] Guid? sprintId,
        [FromQuery] Core.Enums.WorkItemType? type,
        [FromQuery] Core.Enums.WorkItemStatus? status)
    {
        var query = _context.WorkItems
            .Include(w => w.Assignee)
            .Include(w => w.Component)
            .AsQueryable();

        if (projectId.HasValue) query = query.Where(w => w.ProjectId == projectId);
        if (sprintId.HasValue) query = query.Where(w => w.SprintId == sprintId);
        if (type.HasValue) query = query.Where(w => w.Type == type);
        if (status.HasValue) query = query.Where(w => w.Status == status);

        var items = await query.OrderBy(w => w.OrderIndex).ToListAsync();

        return Ok(items.Select(w => new WorkItemDto(
            w.Id, w.Title, w.Description, w.Type, w.Status, w.Priority,
            w.StoryPoints, w.EstimatedHours, w.DueDate,
            w.ProjectId, w.SprintId, w.Assignee?.FullName, w.Component?.Name
        )));
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<WorkItemDto>> GetWorkItem(Guid id)
    {
        var item = await _context.WorkItems
            .Include(w => w.Assignee)
            .Include(w => w.Component)
            .Include(w => w.Comments).ThenInclude(c => c.Author)
            .Include(w => w.Checklists).ThenInclude(c => c.Items)
            .FirstOrDefaultAsync(w => w.Id == id);

        if (item == null) return NotFound();

        return Ok(new
        {
            Id = item.Id,
            Title = item.Title,
            Description = item.Description,
            Type = item.Type,
            Status = item.Status,
            Priority = item.Priority,
            StoryPoints = item.StoryPoints,
            EstimatedHours = item.EstimatedHours,
            ActualHours = item.ActualHours,
            DueDate = item.DueDate,
            AcceptanceCriteria = item.AcceptanceCriteria,
            ProjectId = item.ProjectId,
            SprintId = item.SprintId,
            Assignee = item.Assignee != null ? new { item.Assignee.Id, item.Assignee.FullName, item.Assignee.AvatarUrl } : null,
            Component = item.Component != null ? new { item.Component.Id, item.Component.Name } : null,
            Comments = item.Comments.Select(c => new
            {
                c.Id, c.Content, c.CreatedAt, c.IsEdited,
                Author = new { c.Author!.Id, c.Author.FullName, c.Author.AvatarUrl }
            }),
            Checklists = item.Checklists.Select(cl => new
            {
                cl.Id, cl.Title,
                Items = cl.Items.Select(i => new { i.Id, i.Content, i.IsCompleted, i.CompletedAt })
            }),
            CreatedAt = item.CreatedAt,
            UpdatedAt = item.UpdatedAt
        });
    }

    [HttpPost]
    public async Task<ActionResult<WorkItemDto>> CreateWorkItem(CreateWorkItemDto dto)
    {
        var maxOrder = await _context.WorkItems
            .Where(w => w.ProjectId == dto.ProjectId)
            .MaxAsync(w => (int?)w.OrderIndex) ?? 0;

        var item = new WorkItem
        {
            Title = dto.Title,
            Description = dto.Description,
            Type = dto.Type,
            Priority = dto.Priority,
            StoryPoints = dto.StoryPoints,
            EstimatedHours = dto.EstimatedHours,
            DueDate = dto.DueDate,
            AcceptanceCriteria = dto.AcceptanceCriteria,
            ProjectId = dto.ProjectId,
            SprintId = dto.SprintId,
            AssigneeId = dto.AssigneeId,
            ParentWorkItemId = dto.ParentWorkItemId,
            ComponentId = dto.ComponentId,
            OrderIndex = maxOrder + 1
        };

        _context.WorkItems.Add(item);
        await _context.SaveChangesAsync();

        return CreatedAtAction(nameof(GetWorkItem), new { id = item.Id }, new WorkItemDto(
            item.Id, item.Title, item.Description, item.Type, item.Status,
            item.Priority, item.StoryPoints, item.EstimatedHours, item.DueDate,
            item.ProjectId, item.SprintId, null, null
        ));
    }

    [HttpPut("{id}/status")]
    public async Task<IActionResult> UpdateStatus(Guid id, [FromBody] Core.Enums.WorkItemStatus status)
    {
        var item = await _context.WorkItems.FindAsync(id);
        if (item == null) return NotFound();

        var oldStatus = item.Status;
        item.Status = status;
        item.UpdatedAt = DateTime.UtcNow;

        if (status == Core.Enums.WorkItemStatus.InProgress && !item.StartedAt.HasValue)
            item.StartedAt = DateTime.UtcNow;

        if (status == Core.Enums.WorkItemStatus.Done && !item.CompletedAt.HasValue)
            item.CompletedAt = DateTime.UtcNow;

        // Add history
        _context.WorkItemHistories.Add(new WorkItemHistory
        {
            WorkItemId = id,
            FieldName = "Status",
            OldValue = oldStatus.ToString(),
            NewValue = status.ToString()
        });

        await _context.SaveChangesAsync();
        return NoContent();
    }

    [HttpPut("{id}/sprint")]
    public async Task<IActionResult> MoveToSprint(Guid id, [FromBody] Guid? sprintId)
    {
        var item = await _context.WorkItems.FindAsync(id);
        if (item == null) return NotFound();

        item.SprintId = sprintId;
        item.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        return NoContent();
    }

    [HttpPost("{id}/comments")]
    public async Task<IActionResult> AddComment(Guid id, [FromBody] CreateCommentRequest request)
    {
        var item = await _context.WorkItems.FindAsync(id);
        if (item == null) return NotFound();

        var comment = new Comment
        {
            Content = request.Content,
            WorkItemId = id,
            AuthorId = request.AuthorId
        };

        _context.Comments.Add(comment);
        await _context.SaveChangesAsync();

        return Ok(new { comment.Id, comment.Content, comment.CreatedAt });
    }
}

public record CreateCommentRequest(string Content, Guid AuthorId);
