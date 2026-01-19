namespace SynapsePlatform.Core.Entities;

/// <summary>
/// Represents a comment on a work item
/// </summary>
public class Comment : BaseEntity
{
    public string Content { get; set; } = string.Empty;
    public bool IsEdited { get; set; } = false;

    // Foreign keys
    public Guid WorkItemId { get; set; }
    public Guid AuthorId { get; set; }
    public Guid? ParentCommentId { get; set; }

    // Navigation
    public virtual WorkItem? WorkItem { get; set; }
    public virtual ApplicationUser? Author { get; set; }
    public virtual Comment? ParentComment { get; set; }
    public virtual ICollection<Comment> Replies { get; set; } = new List<Comment>();
}

/// <summary>
/// Represents an attachment
/// </summary>
public class Attachment : BaseEntity
{
    public string FileName { get; set; } = string.Empty;
    public string? OriginalFileName { get; set; }
    public string? ContentType { get; set; }
    public long FileSize { get; set; }
    public string StoragePath { get; set; } = string.Empty;
    public string? ThumbnailPath { get; set; }

    // Foreign keys
    public Guid WorkItemId { get; set; }
    public Guid UploadedById { get; set; }

    // Navigation
    public virtual WorkItem? WorkItem { get; set; }
    public virtual ApplicationUser? UploadedBy { get; set; }
}

/// <summary>
/// Work item history for audit trail
/// </summary>
public class WorkItemHistory : BaseEntity
{
    public string FieldName { get; set; } = string.Empty;
    public string? OldValue { get; set; }
    public string? NewValue { get; set; }
    public string? ChangeSummary { get; set; }

    // Foreign keys
    public Guid WorkItemId { get; set; }
    public Guid ChangedById { get; set; }

    // Navigation
    public virtual WorkItem? WorkItem { get; set; }
    public virtual ApplicationUser? ChangedBy { get; set; }
}

/// <summary>
/// Checklist within a work item
/// </summary>
public class Checklist : BaseEntity
{
    public string Title { get; set; } = string.Empty;
    public int OrderIndex { get; set; }

    // Foreign keys
    public Guid WorkItemId { get; set; }

    // Navigation
    public virtual WorkItem? WorkItem { get; set; }
    public virtual ICollection<ChecklistItem> Items { get; set; } = new List<ChecklistItem>();
}

/// <summary>
/// Individual checklist item
/// </summary>
public class ChecklistItem : BaseEntity
{
    public string Content { get; set; } = string.Empty;
    public bool IsCompleted { get; set; } = false;
    public int OrderIndex { get; set; }
    public DateTime? CompletedAt { get; set; }
    public Guid? CompletedById { get; set; }

    // Foreign keys
    public Guid ChecklistId { get; set; }

    // Navigation
    public virtual Checklist? Checklist { get; set; }
    public virtual ApplicationUser? CompletedBy { get; set; }
}
