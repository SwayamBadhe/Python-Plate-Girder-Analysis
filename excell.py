import numpy as np
import pandas as pd
import methods

Zp_case3 = 0

# Input data from the user
def inputDefaultValues():
    unsupported_length_m = float(input("Enter the Unsupported Length of the beam (in meters): "))
    yield_strength_MPa = float(input("Enter the Yield strength of steel (in MPa): "))
    partial_safety_factor = float(input("Enter the Partial Safety Factor: "))
    modulus_of_elasticity_N_per_mm2 = float(input("Enter the Modulus of elasticity of Steel (in N/mm^2): "))
    bearing_support_width_mm = float(input("Enter the Width of column or bearing support (in millimeters): "))
    
    return (unsupported_length_m, yield_strength_MPa, partial_safety_factor, modulus_of_elasticity_N_per_mm2, bearing_support_width_mm)

def input_bending_moment():
    max_moment_mid_span_kNm = float(input("Enter Max Bending moment at Mid Span (in kNm): "))
    max_moment_support_kNm = float(input("Enter Max Bending Moment at support (in kNm): "))
    max_shear_force_kN = float(input("Enter Maximum Shear Force (in kN): "))

    return (max_moment_mid_span_kNm, max_moment_support_kNm, max_shear_force_kN)  

def input_plate_sizes():
    depth_mm = float(input("Enter Plate Depth (in mm): "))
    flange_width_mm = float(input("Enter Plate Flange Depth (in mm): "))
    flange_thickness_mm = float(input("Enter Plate Flange Thickness (in mm): "))
    web_thickness_mm = float(input("Enter Plate Web Thickness (in mm): "))

    return (depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm)


# Function to write data to CSV
def write_to_csv(filename, data):
    df = pd.DataFrame(data, columns=['Parameter', 'Value'])
    df.to_csv(filename, index=False)

def append_to_csv(filename, data):
    df = pd.DataFrame(data, columns=['Parameter', 'Value'])
    with open(filename, 'a', newline='') as file:
        file.write("-" * 60 + "\n")  # Add separator line
        df.to_csv(file, index=False, header=False)

initial_values_input_bool = input("Do you want to use preset values?: ")
if (initial_values_input_bool == "n" or initial_values_input_bool == "N"):
    unsupported_length_m, yield_strength_MPa, partial_safety_factor, modulus_of_elasticity_N_per_mm2, bearing_support_width_mm = inputDefaultValues()
    methods.setInitialValues(unsupported_length_m, yield_strength_MPa, partial_safety_factor, modulus_of_elasticity_N_per_mm2, bearing_support_width_mm)

while (True):

    calculation_type = input('''
                            1. Effective length of Beam L (c/c of column support)
                                (Type - Beam L)
                            2. Input Calculations of Bending Moment 
                                (Type - Bending Moment Input)
                            3. Plastic Section Modulus Required,Zp
                                (Type - Plastic Section)
                            4. Selection of suitable Plate Sizes
                                (Type - Suitable Plate Sizes)
                            Enter your choice: 
                        ''')

    def switch(calculation_type): 
        global Zp_case3     

        initial_values = methods.getInitialValues()
        unsupported_length_m = initial_values["unsupported_length_m"]
        yield_strength_MPa = initial_values["yield_strength_MPa"]
        partial_safety_factor = initial_values["partial_safety_factor"]
        modulus_of_elasticity_N_per_mm2 = initial_values["modulus_of_elasticity_N_per_mm2"]
        bearing_support_width_mm = initial_values["bearing_support_width_mm"]  

        bending_moment_inital_values = methods.getLocalValues2()
        max_moment_mid_span_kNm = bending_moment_inital_values["max_moment_mid_span_kNm"]
        max_moment_support_kNm = bending_moment_inital_values["max_moment_support_kNm"]
        max_shear_force_kN = bending_moment_inital_values["max_shear_force_kN"]

        plate_size_initial_values = methods.getLocalValues4()
        depth_mm = plate_size_initial_values["depth_mm"]
        flange_width_mm = plate_size_initial_values["flange_width_mm"]
        flange_thickness_mm = plate_size_initial_values["flange_thickness_mm"]
        web_thickness_mm = plate_size_initial_values["web_thickness_mm"]

        if (calculation_type == "Beam L" or calculation_type == "1"):            
            L = methods.calculate_effective_length(unsupported_length_m, bearing_support_width_mm)
            print(f"Effective length of Beam L (c/c of column support): {L} meters")

            # Prepare data for writing to CSV
            data = [
                ("Unsupported Length of the beam (m): ", unsupported_length_m),
                ("Yield strength of steel (MPa): ", yield_strength_MPa),
                ("Partial Safety Factor: ", partial_safety_factor),
                ("Modulus of elasticity of Steel (N/mm^2): ", modulus_of_elasticity_N_per_mm2),
                ("Width of column or bearing support (mm): ", bearing_support_width_mm),
                ("Effective length of Beam L (m): ", L)
            ]

            # Write data to CSV file
            write_to_csv('results.csv', data)

        elif (calculation_type == "Bending Moment" or calculation_type == "2"):
            bending_moment_input_bool = input("Do you want to use preset values?: ")
            if (bending_moment_input_bool == "n" or bending_moment_input_bool == "N"):
                max_moment_mid_span_kNm, max_moment_support_kNm, max_shear_force_kN = input_bending_moment()
                methods.setLocalValues2(max_moment_mid_span_kNm, max_moment_support_kNm, max_shear_force_kN)
            
            methods.setLocalValues3(max_moment_mid_span_kNm, max_moment_support_kNm)
            

            data = [
                ("Max Bending moment at Mid Span (kNm): ", max_moment_mid_span_kNm),
                ("Max Bending Moment at support (KNm): ", max_moment_support_kNm),
                ("Maximum Shear Force (Kn): ", max_shear_force_kN)
            ]

            # append data to CSV file
            append_to_csv('results.csv', data)
        
        elif (calculation_type == "Plastic Section" or calculation_type == "3"):
            max_moment_kNm = max(max_moment_mid_span_kNm, max_moment_support_kNm)

            # Calculate Zp
            Zp_case3 =  Zp = methods.ZpFunc(max_moment_kNm, partial_safety_factor, yield_strength_MPa)

            print(f"Max Moment of mid and support Moment: {max_moment_kNm} KNm")
            print(f"Plastic Section Modulus Required (Zp): {Zp} mm^3")


            # Prepare data for writing to CSV
            data = [
                ("Max Moment (kNm): ", max_moment_kNm),
                ("Partial Safety Factor: ", partial_safety_factor),
                ("Yield Strength of Steel (MPa): ", yield_strength_MPa),
                ("MAx Moment of mid nad support Moment: ", max_moment_kNm),
                ("Plastic Section Modulus Required (mm^3): ", Zp)
            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)

        elif (calculation_type == "Suitable Plate Sizes" or calculation_type == "4"):
            plate_size_input_bool = input("Do you want to use preset values?: ")
            if (plate_size_input_bool == "n" or plate_size_input_bool == "N"):
                depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm = input_plate_sizes()
                methods.setLocalValues4(depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm)
            
            plate_properties = methods.calculate_plate_properties(depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm, yield_strength_MPa)

            web_depth_mm = plate_properties["web_depth_mm"]
            Ix = plate_properties["Ix"]
            Iy = plate_properties["Iy"]
            epsilon = plate_properties["epsilon"]
            Ze = plate_properties["Ze"]
            Zp = plate_properties["Zp"]

            print(f"Web Depth: {web_depth_mm} mm")
            print(f"Moment of Inertia about major axis (Ix): {Ix} mm^4")
            print(f"Moment of Inertia about weak or minor axis (Iy): {Iy} mm^4")
            print(f"Epsilon: {epsilon}")
            print(f"Elastic Section Modulus (Ze): {Ze} mm^3")
            print(f"Plastic Section Modulus (Zp): {Zp} mm^3")    

            if (Zp >= Zp_case3):
                print("Provided section is ok")
                msg = "Provided section is ok"
            else:
                print("Revise the section")
                msg = "Revise the section"

            data = [
                ("Web Depth (mm): ", web_depth_mm),
                ("Moment of Inertia about major axis (Ix) (mm^4): ", Ix),
                ("Moment of Inertia about weak or minor axis (Iy) (mm^4): ", Iy),
                ("Epsilon: ", epsilon),
                ("Elastic Section Modulus (Ze) (mm^3): ", Ze),
                ("Plastic Section Modulus (Zp) (mm^3): ", Zp),
                ("Message: ", msg)
            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)


    switch(calculation_type)

