/**
 * SYNAPSE Neural Connection Layer - Hardware-Software Balancing Algorithm
 * ========================================================================
 *
 * C++ implementation for embedded systems and high-performance scenarios.
 *
 * Bu algoritma, donanım kısıtları ile yazılım hızı arasında optimal
 * dengeyi sağlar. Gerçek zamanlı sistemlerde kullanım için optimize edilmiştir.
 *
 * Author: SYNAPSE Framework Team
 * License: MIT
 */

#ifndef SYNAPSE_BALANCING_ALGORITHM_HPP
#define SYNAPSE_BALANCING_ALGORITHM_HPP

#include <cmath>
#include <deque>
#include <vector>
#include <chrono>
#include <functional>
#include <optional>
#include <string>
#include <mutex>
#include <atomic>

namespace synapse {
namespace neural {

// =============================================================================
// CONSTANTS & THRESHOLDS
// =============================================================================

struct Thresholds {
    // IDI Thresholds
    static constexpr double IDI_HEALTHY = 3.0;
    static constexpr double IDI_WARNING = 5.0;
    static constexpr double IDI_CRITICAL = 7.0;
    static constexpr double IDI_QUARANTINE = 10.0;

    // Hardware Constraints
    static constexpr double CPU_WARNING = 70.0;
    static constexpr double CPU_CRITICAL = 85.0;
    static constexpr double CPU_EMERGENCY = 95.0;

    static constexpr double MEMORY_WARNING = 75.0;
    static constexpr double MEMORY_CRITICAL = 90.0;

    static constexpr double TEMPERATURE_WARNING = 70.0;
    static constexpr double TEMPERATURE_CRITICAL = 85.0;
    static constexpr double TEMPERATURE_SHUTDOWN = 95.0;

    // Balancing
    static constexpr double HW_SW_IMBALANCE_THRESHOLD = 0.3;
    static constexpr double LATENCY_WARNING_MS = 100.0;
    static constexpr double LATENCY_CRITICAL_MS = 500.0;
};

// =============================================================================
// ENUMS
// =============================================================================

enum class SeverityLevel {
    HEALTHY,
    WARNING,
    CRITICAL,
    QUARANTINE
};

enum class MitigationAction {
    NONE,
    THROTTLE,
    BRAKE,
    QUARANTINE,
    REBALANCE,
    ALERT,
    AUTO_INTEGRATE
};

enum class ComponentType {
    HARDWARE,
    SOFTWARE,
    FIRMWARE,
    HYBRID
};

// =============================================================================
// DATA STRUCTURES
// =============================================================================

struct TelemetryData {
    std::string component_id;
    std::chrono::system_clock::time_point timestamp;

    double cpu_usage;           // 0-100
    double memory_usage;        // 0-100
    double io_latency_ms;
    double network_latency_ms;
    double error_rate;          // 0-1
    double throughput;          // requests/sec

    std::optional<double> temperature;      // Hardware only (Celsius)
    std::optional<double> power_consumption; // Hardware only (Watts)
};

struct MitigationResult {
    MitigationAction action;
    std::string component_id;
    std::string reason;
    std::chrono::system_clock::time_point timestamp;

    // Extended details
    double idi_score = 0.0;
    double throttle_level = 1.0;
    double imbalance = 0.0;
};

struct BalanceMetrics {
    double hw_capacity;
    double sw_demand;
    double imbalance;
    std::chrono::system_clock::time_point timestamp;
};

// =============================================================================
// IDI CALCULATOR
// =============================================================================

/**
 * Integration Debt Index Calculator
 *
 * Formula: IDI = (Days Since Last Integration) × (LoC Changed / 1000) × (Dependencies / 10)
 */
class IDICalculator {
public:
    static double calculate(int days, int loc_changed, int dependencies) {
        double d = std::max(days, 0);
        double l = std::max(loc_changed, 0) / 1000.0;
        double dep = std::max(dependencies, 1) / 10.0;

        return d * l * dep;
    }

    static SeverityLevel getSeverity(double idi) {
        if (idi < Thresholds::IDI_HEALTHY) return SeverityLevel::HEALTHY;
        if (idi < Thresholds::IDI_WARNING) return SeverityLevel::WARNING;
        if (idi < Thresholds::IDI_QUARANTINE) return SeverityLevel::CRITICAL;
        return SeverityLevel::QUARANTINE;
    }

    /**
     * Predict future IDI based on current trend
     */
    static double predictIDI(int current_days, int current_loc, int dependencies,
                             int days_ahead, double daily_loc_rate) {
        int future_days = current_days + days_ahead;
        int future_loc = current_loc + static_cast<int>(daily_loc_rate * days_ahead);
        return calculate(future_days, future_loc, dependencies);
    }
};

// =============================================================================
// PID CONTROLLER
// =============================================================================

/**
 * PID Controller for Adaptive Throttling
 *
 * Sistem yüküne göre dinamik throttle ayarlaması yapar.
 */
class PIDController {
private:
    double kp_, ki_, kd_;
    double integral_ = 0.0;
    double previous_error_ = 0.0;
    double target_;

    // Anti-windup limits
    static constexpr double INTEGRAL_MIN = -50.0;
    static constexpr double INTEGRAL_MAX = 50.0;

public:
    PIDController(double kp = 0.5, double ki = 0.1, double kd = 0.05, double target = 70.0)
        : kp_(kp), ki_(ki), kd_(kd), target_(target) {}

    void setTarget(double target) { target_ = target; }

    void reset() {
        integral_ = 0.0;
        previous_error_ = 0.0;
    }

    /**
     * Calculate throttle adjustment
     *
     * @param current_value Current utilization value
     * @return Adjustment value (-0.3 to +0.3)
     */
    double calculate(double current_value) {
        double error = target_ - current_value;

        // Proportional term
        double p_term = kp_ * error;

        // Integral term with anti-windup
        integral_ = std::clamp(integral_ + error, INTEGRAL_MIN, INTEGRAL_MAX);
        double i_term = ki_ * integral_;

        // Derivative term
        double d_term = kd_ * (error - previous_error_);
        previous_error_ = error;

        // Combined PID output, normalized
        double adjustment = (p_term + i_term + d_term) / 100.0;

        // Clamp to reasonable range
        return std::clamp(adjustment, -0.3, 0.3);
    }
};

// =============================================================================
// HARDWARE-SOFTWARE BALANCER
// =============================================================================

/**
 * Hardware-Software Balancing Algorithm
 *
 * Biyolojik homeostasis prensibiyle çalışır:
 * - Donanım kapasitesi (tortoise) - yavaş ama güvenilir
 * - Yazılım talebi (hare) - hızlı ama kaynak tüketir
 * - Amaç: İkisi arasında optimal denge
 */
class HardwareSoftwareBalancer {
private:
    std::deque<BalanceMetrics> history_;
    const size_t moving_avg_window_ = 10;
    mutable std::mutex mutex_;

    double target_throughput_;

public:
    explicit HardwareSoftwareBalancer(double target_throughput = 1000.0)
        : target_throughput_(target_throughput) {}

    /**
     * Calculate hardware capacity score (0-100)
     *
     * Higher score = more capacity available
     */
    double calculateHardwareCapacity(const TelemetryData& telemetry) const {
        // CPU capacity (inverse)
        double cpu_capacity = 100.0 - telemetry.cpu_usage;

        // Memory capacity (inverse)
        double memory_capacity = 100.0 - telemetry.memory_usage;

        // Temperature factor
        double temp_factor = 1.0;
        if (telemetry.temperature.has_value()) {
            double temp = telemetry.temperature.value();
            if (temp > Thresholds::TEMPERATURE_CRITICAL) {
                temp_factor = 0.3;
            } else if (temp > Thresholds::TEMPERATURE_WARNING) {
                temp_factor = 0.7;
            }
        }

        // Weighted average
        return (cpu_capacity * 0.4) + (memory_capacity * 0.4) + (100.0 * temp_factor * 0.2);
    }

    /**
     * Calculate software demand score (0-100)
     *
     * Higher score = more resources demanded
     */
    double calculateSoftwareDemand(const TelemetryData& telemetry) const {
        // Throughput-based demand
        double throughput_demand = std::min(
            (telemetry.throughput / target_throughput_) * 100.0, 100.0);

        // Latency-based urgency
        double latency_urgency;
        if (telemetry.io_latency_ms > Thresholds::LATENCY_CRITICAL_MS) {
            latency_urgency = 100.0;
        } else if (telemetry.io_latency_ms > Thresholds::LATENCY_WARNING_MS) {
            latency_urgency = 70.0;
        } else {
            latency_urgency = (telemetry.io_latency_ms / Thresholds::LATENCY_WARNING_MS) * 50.0;
        }

        // Error rate-based stress
        double error_stress = std::min(telemetry.error_rate * 1000.0, 100.0);

        // Weighted average
        return (throughput_demand * 0.5) + (latency_urgency * 0.3) + (error_stress * 0.2);
    }

    /**
     * Calculate imbalance score (-1 to +1)
     *
     * Negative = Hardware insufficient (software too fast)
     * Positive = Hardware idle (software too slow)
     * Zero = Balanced
     */
    double calculateImbalance(double hw_capacity, double sw_demand) const {
        if (hw_capacity + sw_demand == 0.0) return 0.0;
        return (hw_capacity - sw_demand) / 100.0;
    }

    /**
     * Get balancing action based on imbalance
     */
    MitigationResult getBalancingAction(double imbalance,
                                         const std::string& component_id,
                                         double current_throttle) const {
        MitigationResult result;
        result.component_id = component_id;
        result.timestamp = std::chrono::system_clock::now();
        result.imbalance = imbalance;

        const double threshold = Thresholds::HW_SW_IMBALANCE_THRESHOLD;

        if (std::abs(imbalance) < threshold) {
            // Balanced
            result.action = MitigationAction::NONE;
            result.reason = "System is balanced";
            result.throttle_level = current_throttle;
        }
        else if (imbalance < -threshold) {
            // Hardware overloaded - throttle software
            double throttle_amount = std::min(std::abs(imbalance), 0.5);
            double new_throttle = std::max(current_throttle - throttle_amount, 0.2);

            result.action = MitigationAction::THROTTLE;
            result.reason = "Hardware overloaded - throttling software";
            result.throttle_level = new_throttle;
        }
        else {
            // Hardware underutilized - can boost
            double boost_potential = std::min(imbalance, 0.3);

            result.action = MitigationAction::ALERT;
            result.reason = "Hardware underutilized - boost potential available";
            result.throttle_level = std::min(current_throttle + boost_potential, 1.0);
        }

        return result;
    }

    /**
     * Main balancing function - call on each telemetry update
     */
    MitigationResult balance(const TelemetryData& telemetry, double current_throttle) {
        double hw_capacity = calculateHardwareCapacity(telemetry);
        double sw_demand = calculateSoftwareDemand(telemetry);
        double imbalance = calculateImbalance(hw_capacity, sw_demand);

        // Record to history
        {
            std::lock_guard<std::mutex> lock(mutex_);
            history_.push_back({
                hw_capacity,
                sw_demand,
                imbalance,
                std::chrono::system_clock::now()
            });

            // Keep history bounded
            while (history_.size() > moving_avg_window_ * 2) {
                history_.pop_front();
            }
        }

        // Calculate smoothed imbalance (moving average)
        double avg_imbalance = imbalance;
        {
            std::lock_guard<std::mutex> lock(mutex_);
            if (history_.size() >= moving_avg_window_) {
                double sum = 0.0;
                auto it = history_.end();
                std::advance(it, -static_cast<int>(moving_avg_window_));
                for (; it != history_.end(); ++it) {
                    sum += it->imbalance;
                }
                avg_imbalance = sum / moving_avg_window_;
            }
        }

        return getBalancingAction(avg_imbalance, telemetry.component_id, current_throttle);
    }

    /**
     * Get recent balance metrics
     */
    std::vector<BalanceMetrics> getRecentMetrics(size_t count = 10) const {
        std::lock_guard<std::mutex> lock(mutex_);
        std::vector<BalanceMetrics> result;

        auto start = history_.size() > count
            ? history_.end() - count
            : history_.begin();

        for (auto it = start; it != history_.end(); ++it) {
            result.push_back(*it);
        }

        return result;
    }
};

// =============================================================================
// IDI BRAKE
// =============================================================================

/**
 * IDI Brake - Automatic slowdown when integration debt rises
 *
 * Biyolojik analoji: Vücuttaki ağrı sinyali
 * IDI yükseldiğinde sistem otomatik olarak yavaşlar.
 */
class IDIBrake {
public:
    /**
     * Calculate throttle level based on IDI
     *
     * @param idi Integration Debt Index value
     * @return Throttle level (0.0 = stopped, 1.0 = full speed)
     */
    static double calculateThrottleLevel(double idi) {
        if (idi < Thresholds::IDI_HEALTHY) {
            return 1.0;  // Full speed
        }

        if (idi < Thresholds::IDI_WARNING) {
            // Linear slowdown from 1.0 to 0.7
            double ratio = (idi - Thresholds::IDI_HEALTHY) /
                          (Thresholds::IDI_WARNING - Thresholds::IDI_HEALTHY);
            return 1.0 - (ratio * 0.3);
        }

        if (idi < Thresholds::IDI_CRITICAL) {
            // Aggressive slowdown from 0.7 to 0.3
            double ratio = (idi - Thresholds::IDI_WARNING) /
                          (Thresholds::IDI_CRITICAL - Thresholds::IDI_WARNING);
            return 0.7 - (ratio * 0.4);
        }

        if (idi < Thresholds::IDI_QUARANTINE) {
            // Near stop from 0.3 to 0.1
            double ratio = (idi - Thresholds::IDI_CRITICAL) /
                          (Thresholds::IDI_QUARANTINE - Thresholds::IDI_CRITICAL);
            return 0.3 - (ratio * 0.2);
        }

        return 0.0;  // Full stop - quarantine
    }

    /**
     * Apply brake and get mitigation result
     */
    static MitigationResult applyBrake(const std::string& component_id,
                                        double idi,
                                        int days_since_integration,
                                        int loc_changed,
                                        int dependencies) {
        MitigationResult result;
        result.component_id = component_id;
        result.timestamp = std::chrono::system_clock::now();
        result.idi_score = idi;

        SeverityLevel severity = IDICalculator::getSeverity(idi);
        double throttle = calculateThrottleLevel(idi);
        result.throttle_level = throttle;

        switch (severity) {
            case SeverityLevel::QUARANTINE:
                result.action = MitigationAction::QUARANTINE;
                result.reason = "IDI exceeded quarantine threshold - component isolated";
                break;

            case SeverityLevel::CRITICAL:
                result.action = MitigationAction::BRAKE;
                result.reason = "IDI in critical zone - hard brake applied";
                break;

            case SeverityLevel::WARNING:
                result.action = MitigationAction::THROTTLE;
                result.reason = "IDI in warning zone - soft throttle applied";
                break;

            default:
                result.action = MitigationAction::NONE;
                result.reason = "IDI healthy - no mitigation needed";
                break;
        }

        return result;
    }
};

// =============================================================================
// NEURAL PRUNING
// =============================================================================

/**
 * Neural Pruning - Automatic quarantine mechanism
 *
 * Biyolojik analoji: Sinaptik budama
 * Sorunlu bileşenler otomatik olarak izole edilir.
 */
class NeuralPruning {
public:
    struct QuarantineEntry {
        std::string component_id;
        std::string reason;
        std::chrono::system_clock::time_point quarantined_at;
        double idi_at_quarantine;
        double health_at_quarantine;
    };

    /**
     * Check if component should be pruned
     */
    static bool shouldPrune(double idi,
                           double error_rate,
                           double health_score,
                           std::optional<double> temperature = std::nullopt) {
        // IDI check
        if (idi >= Thresholds::IDI_QUARANTINE) return true;

        // Error rate check
        if (error_rate >= 0.05) return true;  // 5% error rate

        // Temperature check (for hardware)
        if (temperature.has_value() &&
            temperature.value() >= Thresholds::TEMPERATURE_SHUTDOWN) {
            return true;
        }

        // Health score check
        if (health_score < 20.0) return true;

        return false;
    }

    /**
     * Check if component can be restored from quarantine
     */
    static bool canRestore(double idi,
                          double health_score,
                          std::chrono::system_clock::time_point quarantined_at) {
        // IDI must be below warning
        if (idi >= Thresholds::IDI_WARNING) return false;

        // Health must be above 70
        if (health_score < 70.0) return false;

        // Minimum quarantine time (1 hour)
        auto now = std::chrono::system_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::hours>(now - quarantined_at);
        if (duration.count() < 1) return false;

        return true;
    }
};

// =============================================================================
// COMBINED THROTTLE CALCULATOR
// =============================================================================

/**
 * Combined Throttle Calculator
 *
 * IDI Brake ve HW-SW Balance sonuçlarını birleştirerek
 * nihai throttle değerini hesaplar.
 */
class CombinedThrottleCalculator {
public:
    /**
     * Calculate final throttle level considering all factors
     *
     * @param idi_throttle Throttle from IDI Brake
     * @param balance_throttle Throttle from HW-SW Balance
     * @param is_quarantined Whether component is quarantined
     * @return Final throttle level (0.0 to 1.0)
     */
    static double calculate(double idi_throttle,
                           double balance_throttle,
                           bool is_quarantined) {
        if (is_quarantined) {
            return 0.0;
        }

        // Take the more restrictive throttle
        double min_throttle = std::min(idi_throttle, balance_throttle);

        // Apply smoothing to avoid sudden changes
        // In real implementation, this would use previous value
        return min_throttle;
    }
};

// =============================================================================
// WEBSOCKET EVENT HELPERS
// =============================================================================

namespace events {
    constexpr const char* TELEMETRY_UPDATE = "telemetry:update";
    constexpr const char* IDI_UPDATE = "idi:update";
    constexpr const char* MITIGATION_TRIGGERED = "mitigation:triggered";
    constexpr const char* COMPONENT_QUARANTINED = "component:quarantined";
    constexpr const char* COMPONENT_RESTORED = "component:restored";
    constexpr const char* SYSTEM_HEALTH_UPDATE = "system:health";
    constexpr const char* BALANCE_UPDATE = "balance:update";
}

} // namespace neural
} // namespace synapse

#endif // SYNAPSE_BALANCING_ALGORITHM_HPP
