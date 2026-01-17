namespace SynapsePlatform.Core.Entities;

public class Organization : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? LogoUrl { get; set; }
    public string? Website { get; set; }

    public virtual ICollection<Portfolio> Portfolios { get; set; } = new List<Portfolio>();
    public virtual ICollection<Team> Teams { get; set; } = new List<Team>();
    public virtual ICollection<ApplicationUser> Users { get; set; } = new List<ApplicationUser>();
}
