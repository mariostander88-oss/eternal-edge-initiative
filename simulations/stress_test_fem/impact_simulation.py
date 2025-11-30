import numpy as np
import matplotlib.pyplot as plt

def generate_stress_strain(strain_array, modulus_gpa, yield_strength_gpa, plastic_limit):
    """
    Generates a simplified stress-strain curve.
    Modulus: Stiffness (slope of the line)
    Yield Strength: Point where it permanently bends
    Plastic Limit: Point where it breaks
    """
    stress = []
    yield_strain = yield_strength_gpa / modulus_gpa
    
    for strain in strain_array:
        if strain <= yield_strain:
            # Elastic Region (It bounces back)
            s = strain * modulus_gpa
        elif strain <= plastic_limit:
            # Plastic Region (It bends permanently)
            # Add slight work hardening for realism
            s = yield_strength_gpa + (strain - yield_strain) * 10 
        else:
            # Fracture (It breaks)
            s = None 
        stress.append(s)
    return stress

def main():
    # --- Simulation Setup ---
    # Strain range from 0% to 5% deformation
    strain = np.linspace(0, 0.05, 500) 
    
    # --- Material 1: High-Carbon Steel (The Competitor) ---
    # Stiff but yields early (bends easily)
    steel_stress = generate_stress_strain(
        strain_array=strain,
        modulus_gpa=210,      # Standard steel stiffness
        yield_strength_gpa=0.8, # Yields at 800 MPa
        plastic_limit=0.035   # Breaks at 3.5% strain
    )
    
    # --- Material 2: Cape Town Alloy (HEA-BMG Hybrid) ---
    # Less stiff (flexes) but insanely strong before yielding
    alloy_stress = generate_stress_strain(
        strain_array=strain,
        modulus_gpa=110,      # Titanium-based stiffness
        yield_strength_gpa=2.2, # Yields at 2.2 GPa (Very High!)
        plastic_limit=0.045   # Toughened by HEA phase to resist shattering
    )

    # --- Plotting the Impact Resistance ---
    plt.figure(figsize=(10, 6))
    
    plt.plot(strain * 100, steel_stress, 'gray', linestyle='--', linewidth=2, label='High-Carbon Steel (Competitor)')
    plt.plot(strain * 100, alloy_stress, 'purple', linewidth=3, label='Cape Town Alloy (Eternal Edge)')
    
    # Highlight the "Elastic Energy" (The spring effect)
    # The area under the straight line is the energy it can absorb without damage.
    plt.fill_between(strain * 100, alloy_stress, color='purple', alpha=0.1)
    plt.text(1.5, 1.0, "Massive Elastic\nEnergy Absorption", color='purple', fontweight='bold')

    plt.title('Impact Simulation: Stress-Strain Analysis')
    plt.xlabel('Strain (% Deformation)')
    plt.ylabel('Stress (GPa)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 3.0)
    plt.xlim(0, 5.0)
    
    print("Generating Impact_Curve.png...")
    plt.savefig('Impact_Curve.png', dpi=300)
    print("Done.")
    plt.show()

if __name__ == "__main__":
    main()
