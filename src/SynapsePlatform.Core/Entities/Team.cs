namespace SynapsePlatform.Core.Entities;

public class Team : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }

    public Guid OrganizationId { get; set; }
    public Guid? LeaderId { get; set; }

    public virtual Organization? Organization { get; set; }
    public virtual ApplicationUser? Leader { get; set; }
    public virtual ICollection<ApplicationUser> Members { get; set; } = new List<ApplicationUser>();
    public virtual ICollection<Project> Projects { get; set; } = new List<Project>();
}
