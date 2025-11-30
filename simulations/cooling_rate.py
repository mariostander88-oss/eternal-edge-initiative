import numpy as np
import matplotlib.pyplot as plt

def calculate_cooling_path(t, T_start, T_env, rate_constant):
    """
    Simulates cooling using Newton's Law of Cooling.
    T(t) = T_env + (T_start - T_env) * exp(-k * t)
    """
    return T_env + (T_start - T_env) * np.exp(-rate_constant * t)

def main():
    # --- Material Constants (Approximations for Ti-Zr-Ni-Cu) ---
    T_melt = 1500  # Melting point (Kelvin)
    T_nose = 900   # Temperature where crystallization is fastest (Kelvin)
    T_glass = 650  # Glass transition temperature (Kelvin)
    
    # --- Simulation Parameters ---
    time = np.logspace(-4, 0, 500)  # Time from 0.0001s to 1s
    
    # --- 1. Define the "Danger Zone" (Crystallization Nose) ---
    # This is a theoretical curve. If the cooling line touches this, 
    # the alloy crystallizes and fails to become a BMG.
    nose_time = 0.01  # Critical time at the nose (seconds)
    width = 200       # Width of the crystallization curve
    
    # Create a parabolic nose shape in Log-Time space
    T_curve = np.linspace(T_glass, T_melt, 100)
    # Simple mathematical model for a C-curve
    t_curve = nose_time * np.exp(((T_curve - T_nose)**2) / width**2)

    # --- 2. Simulate Cooling Scenarios ---
    
    # Scenario A: Failed Quench (Too Slow)
    # Cooling rate approx 100 K/s - hits the crystals
    T_slow = calculate_cooling_path(time, T_melt, 300, 50) 
    
    # Scenario B: Successful Quench (Eternal Edge Target)
    # Cooling rate approx 10,000 K/s - bypasses the nose
    T_fast = calculate_cooling_path(time, T_melt, 300, 2000) 

    # --- 3. Plotting the TTT Diagram ---
    plt.figure(figsize=(10, 6))
    
    # Plot the Crystallization Nose
    plt.plot(t_curve, T_curve, 'r--', linewidth=2, label='Crystallization Limit (The Nose)')
    plt.fill_betweenx(T_curve, t_curve, 10, color='red', alpha=0.1) # Shade the crystal zone
    
    # Plot Cooling Curves
    plt.plot(time, T_slow, 'orange', label='Standard Casting (Failed)')
    plt.plot(time, T_fast, 'g', linewidth=2.5, label='Hyper-Quench (Glass Formed)')
    
    # Formatting
    plt.xscale('log')
    plt.xlabel('Time (seconds) [Log Scale]')
    plt.ylabel('Temperature (K)')
    plt.title('Critical Cooling Rate Analysis: Ti-Zr-Ni-Cu Alloy')
    plt.axhline(y=T_glass, color='blue', linestyle=':', label='Glass Transition (Tg)')
    plt.axhline(y=T_melt, color='black', linestyle=':', label='Melting Point (Tm)')
    
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.xlim(0.0001, 1)
    plt.ylim(300,
