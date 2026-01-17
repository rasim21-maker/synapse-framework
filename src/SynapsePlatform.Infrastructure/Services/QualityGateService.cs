using Microsoft.EntityFrameworkCore;
using SynapsePlatform.Core.Entities;
using SynapsePlatform.Core.Enums;
using SynapsePlatform.Core.Interfaces;
using SynapsePlatform.Infrastructure.Data;

namespace SynapsePlatform.Infrastructure.Services;

public class QualityGateService : IQualityGateService
{
    private readonly SynapseDbContext _context;

    public QualityGateService(SynapseDbContext context)
    {
        _context = context;
    }

    public async Task<QualityGate> CreateQualityGateAsync(QualityGate gate)
    {
        _context.QualityGates.Add(gate);
        await _context.SaveChangesAsync();
        return gate;
    }

    public async Task<QualityGateResult> CheckQualityGateAsync(
        Guid gateId,
        double actualValue,
        string? commitHash = null)
    {
        var gate = await _context.QualityGates.FindAsync(gateId);
        if (gate == null)
            throw new ArgumentException("Quality gate not found", nameof(gateId));

        var passed = EvaluateThreshold(gate, actualValue);

        var result = new QualityGateResult
        {
            QualityGateId = gateId,
            CheckedAt = DateTime.UtcNow,
            Passed = passed,
            ActualValue = actualValue,
            CommitHash = commitHash,
            Message = passed
                ? $"Quality gate '{gate.Name}' passed. Actual: {actualValue} {gate.ThresholdUnit}"
                : $"Quality gate '{gate.Name}' FAILED. Expected: {gate.ThresholdOperator} {gate.ThresholdValue} {gate.ThresholdUnit}, Actual: {actualValue} {gate.ThresholdUnit}"
        };

        // Update gate status
        gate.LastCheckedAt = DateTime.UtcNow;
        gate.LastCheckPassed = passed;
        gate.LastCheckMessage = result.Message;

        _context.QualityGateResults.Add(result);
        await _context.SaveChangesAsync();

        return result;
    }

    public async Task<IEnumerable<QualityGateResult>> CheckAllProjectGatesAsync(Guid projectId)
    {
        var gates = await _context.QualityGates
            .Where(g => g.ProjectId == projectId && g.IsEnabled)
            .Include(g => g.Component)
            .ToListAsync();

        var results = new List<QualityGateResult>();

        foreach (var gate in gates)
        {
            // Get actual value from component or simulation
            var actualValue = await GetActualValueForGate(gate);
            if (actualValue.HasValue)
            {
                var result = await CheckQualityGateAsync(gate.Id, actualValue.Value);
                results.Add(result);
            }
        }

        return results;
    }

    public async Task<bool> CanProceedWithCommit(Guid projectId, string commitHash)
    {
        var preCommitGates = await _context.QualityGates
            .Where(g => g.ProjectId == projectId
                        && g.IsEnabled
                        && g.Enforcement == QualityGateEnforcement.PreCommitHook)
            .ToListAsync();

        foreach (var gate in preCommitGates)
        {
            var actualValue = await GetActualValueForGate(gate);
            if (actualValue.HasValue)
            {
                var result = await CheckQualityGateAsync(gate.Id, actualValue.Value, commitHash);
                if (!result.Passed && gate.Action == QualityGateAction.RejectCommit)
                {
                    return false;
                }
            }
        }

        return true;
    }

    public async Task<bool> CanProceedWithDeployment(Guid projectId)
    {
        var deploymentGates = await _context.QualityGates
            .Where(g => g.ProjectId == projectId
                        && g.IsEnabled
                        && g.Enforcement == QualityGateEnforcement.Deployment)
            .ToListAsync();

        foreach (var gate in deploymentGates)
        {
            var actualValue = await GetActualValueForGate(gate);
            if (actualValue.HasValue)
            {
                var result = await CheckQualityGateAsync(gate.Id, actualValue.Value);
                if (!result.Passed && gate.Action == QualityGateAction.BlockDeployment)
                {
                    return false;
                }
            }
        }

        return true;
    }

    private bool EvaluateThreshold(QualityGate gate, double actualValue)
    {
        if (!gate.ThresholdValue.HasValue)
            return true;

        return gate.ThresholdOperator switch
        {
            "<=" => actualValue <= gate.ThresholdValue.Value,
            ">=" => actualValue >= gate.ThresholdValue.Value,
            "<" => actualValue < gate.ThresholdValue.Value,
            ">" => actualValue > gate.ThresholdValue.Value,
            "==" => Math.Abs(actualValue - gate.ThresholdValue.Value) < 0.001,
            _ => true
        };
    }

    private async Task<double?> GetActualValueForGate(QualityGate gate)
    {
        if (gate.Component == null)
        {
            // Load component if not included
            await _context.Entry(gate).Reference(g => g.Component).LoadAsync();
        }

        if (gate.Component == null)
            return null;

        return gate.Category.ToLower() switch
        {
            "power_budget" => gate.Component.ActualPowerWatts,
            "thermal" => gate.Component.ActualThermalCelsius,
            "latency" => gate.Component.ActualLatencyMs,
            "memory" => gate.Component.ActualMemoryMB,
            _ => null
        };
    }
}
