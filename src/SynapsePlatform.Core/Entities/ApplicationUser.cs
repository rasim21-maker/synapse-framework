using Microsoft.AspNetCore.Identity;
using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Core.Entities;

public class ApplicationUser : IdentityUser<Guid>
{
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public string? AvatarUrl { get; set; }
    public string? JobTitle { get; set; }
    public UserRole Role { get; set; } = UserRole.Developer;
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public Guid? OrganizationId { get; set; }
    public Guid? TeamId { get; set; }

    public virtual Organization? Organization { get; set; }
    public virtual Team? Team { get; set; }

    public string FullName => $"{FirstName} {LastName}";
}
