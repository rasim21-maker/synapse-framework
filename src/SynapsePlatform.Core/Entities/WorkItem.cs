using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Core.Entities;

public class WorkItem : BaseEntity
{
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public WorkItemType Type { get; set; }
    public WorkItemStatus Status { get; set; } = WorkItemStatus.New;
    public Priority Priority { get; set; } = Priority.Medium;

    public int? StoryPoints { get; set; }
    public double? EstimatedHours { get; set; }
    public double? ActualHours { get; set; }
    public DateTime? DueDate { get; set; }
    public DateTime? StartedAt { get; set; }
    public DateTime? CompletedAt { get; set; }

    public int OrderIndex { get; set; }
    public string? AcceptanceCriteria { get; set; }

    public Guid ProjectId { get; set; }
    public Guid? SprintId { get; set; }
    public Guid? AssigneeId { get; set; }
    public Guid? ReporterId { get; set; }
    public Guid? ParentWorkItemId { get; set; }
    public Guid? ComponentId { get; set; }

    public virtual Project? Project { get; set; }
    public virtual Sprint? Sprint { get; set; }
    public virtual ApplicationUser? Assignee { get; set; }
    public virtual ApplicationUser? Reporter { get; set; }
    public virtual WorkItem? ParentWorkItem { get; set; }
    public virtual Component? Component { get; set; }
    public virtual ICollection<WorkItem> ChildWorkItems { get; set; } = new List<WorkItem>();
    public virtual ICollection<Comment> Comments { get; set; } = new List<Comment>();
    public virtual ICollection<Attachment> Attachments { get; set; } = new List<Attachment>();
    public virtual ICollection<Checklist> Checklists { get; set; } = new List<Checklist>();
    public virtual ICollection<WorkItemHistory> History { get; set; } = new List<WorkItemHistory>();
}
