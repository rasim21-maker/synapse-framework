using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Enums;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Infrastructure.Services;

public class IDIService : IIDIService
{
    private readonly SynapseDbContext _context;

    public IDIService(SynapseDbContext context)
    {
        _context = context;
    }

    // IDI = (Days Since Last Integration) × (LoC Changed / 1000) × (Dependencies / 10)
    public double CalculateComponentIDI(Component component)
    {
        var daysSinceIntegration = component.LastIntegrationDate.HasValue
            ? (DateTime.UtcNow - component.LastIntegrationDate.Value).Days
            : component.DaysSinceLastIntegration;

        var locFactor = component.LinesOfCodeChanged / 1000.0;
        var depFactor = component.DependencyCount / 10.0;

        return daysSinceIntegration * Math.Max(locFactor, 0.1) * Math.Max(depFactor, 0.1);
    }

    public double CalculateProjectIDI(Guid projectId)
    {
        var components = _context.Components
            .Where(c => c.ProjectId == projectId && !c.IsDeleted)
            .ToList();

        if (!components.Any()) return 0;

        return components.Average(c => CalculateComponentIDI(c));
    }

    public async Task<IDIReport> GetIDIReportAsync(Guid projectId)
    {
        var components = await _context.Components
            .Where(c => c.ProjectId == projectId && !c.IsDeleted)
            .ToListAsync();

        var componentInfos = components.Select(c =>
        {
            var idi = CalculateComponentIDI(c);
            return new ComponentIDIInfo
            {
                ComponentId = c.Id,
                ComponentName = c.Name,
                IDI = idi,
                Status = GetIDIStatus(idi),
                DaysSinceLastIntegration = c.LastIntegrationDate.HasValue
                    ? (DateTime.UtcNow - c.LastIntegrationDate.Value).Days
                    : c.DaysSinceLastIntegration
            };
        }).ToList();

        var projectIDI = componentInfos.Any() ? componentInfos.Average(c => c.IDI) : 0;

        // Get trends from integration records
        var trends = await _context.IntegrationRecords
            .Where(r => r.ProjectId == projectId)
            .OrderByDescending(r => r.IntegrationDate)
            .Take(30)
            .Select(r => new IDITrend { Date = r.IntegrationDate, IDI = r.IDIAfterIntegration })
            .ToListAsync();

        return new IDIReport
        {
            ProjectIDI = projectIDI,
            Status = GetIDIStatus(projectIDI),
            Components = componentInfos,
            Trends = trends
        };
    }

    public async Task UpdateComponentIDIAsync(Guid componentId)
    {
        var component = await _context.Components.FindAsync(componentId);
        if (component == null) return;

        component.ComponentIDI = CalculateComponentIDI(component);
        await _context.SaveChangesAsync();
    }

    public async Task<IEnumerable<Component>> GetComponentsNeedingIntegrationAsync(Guid projectId)
    {
        var components = await _context.Components
            .Where(c => c.ProjectId == projectId && !c.IsDeleted)
            .ToListAsync();

        return components.Where(c => CalculateComponentIDI(c) > 3.0).OrderByDescending(c => CalculateComponentIDI(c));
    }

    private static IDIStatus GetIDIStatus(double idi)
    {
        if (idi < 3.0) return IDIStatus.Healthy;
        if (idi <= 5.0) return IDIStatus.Warning;
        return IDIStatus.Critical;
    }
}
