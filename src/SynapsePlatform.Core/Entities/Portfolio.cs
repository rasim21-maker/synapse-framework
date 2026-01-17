namespace SynapsePlatform.Core.Entities;

public class Portfolio : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public double TotalBudget { get; set; }
    public double AllocatedBudget { get; set; }

    public Guid OrganizationId { get; set; }
    public Guid? ManagerId { get; set; }

    public virtual Organization? Organization { get; set; }
    public virtual ApplicationUser? Manager { get; set; }
    public virtual ICollection<Project> Projects { get; set; } = new List<Project>();
}
