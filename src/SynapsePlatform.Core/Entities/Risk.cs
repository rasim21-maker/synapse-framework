using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Core.Entities;

public class Risk : BaseEntity
{
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public RiskLevel Probability { get; set; }
    public RiskLevel Impact { get; set; }
    public RiskStatus Status { get; set; } = RiskStatus.Identified;
    public string? MitigationPlan { get; set; }
    public string? ContingencyPlan { get; set; }
    public DateTime? IdentifiedDate { get; set; }
    public DateTime? TargetResolutionDate { get; set; }

    public Guid ProjectId { get; set; }
    public Guid? OwnerId { get; set; }

    public virtual Project? Project { get; set; }
    public virtual ApplicationUser? Owner { get; set; }

    public int RiskScore => (int)Probability * (int)Impact;
}
