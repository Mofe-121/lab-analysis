import datetime
from typing import Dict, List, Optional, Tuple
import random

class EnvironmentalLabAnalyst:
    def __init__(self):
        # Environmental Impact Assessments (EIA): {eia_id: {"location": str, "date": str, "risks": List[str], "mitigation": Dict, "status": str}}
        self.eia_reports: Dict[str, Dict] = {}

        # Environmental Samples: {sample_id: {"type": str, "location": str, "date_collected": str, "parameters": Dict, "status": str}}
        self.env_samples: Dict[str, Dict] = {}

        # Water Quality Standards: {parameter: {"unit": str, "max_allowed": float, "source": str}}
        self.water_standards: Dict[str, Dict] = {
            "dissolved_oxygen": {"unit": "mg/L", "max_allowed": 5.0, "source": "WHO"},
            "chlorine": {"unit": "mg/L", "max_allowed": 4.0, "source": "EPA"},
            "lead": {"unit": "µg/L", "max_allowed": 10.0, "source": "EPA"},
            "mercury": {"unit": "µg/L", "max_allowed": 2.0, "source": "WHO"},
            "arsenic": {"unit": "µg/L", "max_allowed": 10.0, "source": "WHO"},
            "pH": {"unit": "pH", "max_allowed": 8.5, "min_allowed": 6.5, "source": "EPA"}
        }

        # Lab Equipment: {equipment_id: {"name": str, "type": str, "status": str, "last_calibration": str}}
        self.lab_equipment: Dict[str, Dict] = {}

        # Compliance Reports: {report_id: {"date": str, "samples": List[str], "compliance_status": Dict, "notes": str}}
        self.compliance_reports: Dict[str, Dict] = {}

        # Next IDs for auto-increment
        self.next_eia_id = 1
        self.next_sample_id = 1
        self.next_equipment_id = 1
        self.next_report_id = 1

    # --- Environmental Impact Assessment (EIA) ---
    def create_eia(self, location: str, risks: List[str]) -> str:
        """Create a new Environmental Impact Assessment (EIA) report."""
        eia_id = f"EIA{self.next_eia_id}"
        self.eia_reports[eia_id] = {
            "location": location,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "risks": risks,
            "mitigation": {},
            "status": "Draft"
        }
        self.next_eia_id += 1
        return f"EIA report created for {location} with ID: {eia_id}"

    def add_mitigation_measure(self, eia_id: str, risk: str, measure: str) -> str:
        """Add a mitigation measure for a specific risk in an EIA report."""
        if eia_id in self.eia_reports:
            self.eia_reports[eia_id]["mitigation"][risk] = measure
            return f"Mitigation measure added for risk '{risk}' in EIA {eia_id}"
        return f"EIA ID {eia_id} not found."

    def finalize_eia(self, eia_id: str) -> str:
        """Finalize an EIA report."""
        if eia_id in self.eia_reports:
            self.eia_reports[eia_id]["status"] = "Finalized"
            return f"EIA {eia_id} finalized."
        return f"EIA ID {eia_id} not found."

    # --- Sample Collection and Analysis ---
    def collect_sample(self, sample_type: str, location: str, parameters: List[str]) -> str:
        """Collect an environmental sample for analysis."""
        sample_id = f"SAMP{self.next_sample_id}"
        self.env_samples[sample_id] = {
            "type": sample_type,
            "location": location,
            "date_collected": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "parameters": {param: None for param in parameters},
            "status": "Collected"
        }
        self.next_sample_id += 1
        return f"Sample {sample_type} collected from {location} with ID: {sample_id}"

    def analyze_sample(self, sample_id: str, parameter: str, value: float) -> str:
        """Analyze a specific parameter in an environmental sample."""
        if sample_id in self.env_samples and parameter in self.env_samples[sample_id]["parameters"]:
            self.env_samples[sample_id]["parameters"][parameter] = value
            self.env_samples[sample_id]["status"] = "Analyzed"
            return f"Parameter '{parameter}' analyzed for sample {sample_id}: {value} {self.water_standards.get(parameter, {}).get('unit', '')}"
        return f"Sample ID {sample_id} or parameter '{parameter}' not found."

    # --- Water Quality Measurements ---
    def measure_dissolved_oxygen(self, sample_id: str, do_value: float) -> str:
        """Measure dissolved oxygen (DO) in a water sample."""
        return self.analyze_sample(sample_id, "dissolved_oxygen", do_value)

    def measure_chlorine(self, sample_id: str, chlorine_value: float) -> str:
        """Measure chlorine levels in a water sample."""
        return self.analyze_sample(sample_id, "chlorine", chlorine_value)

    def measure_heavy_metal(self, sample_id: str, metal: str, concentration: float) -> str:
        """Measure heavy metal concentration in a water sample."""
        if metal in ["lead", "mercury", "arsenic"]:
            return self.analyze_sample(sample_id, metal, concentration)
        return f"Heavy metal '{metal}' not supported."

    # --- Compliance Checks ---
    def check_compliance(self, sample_id: str) -> Dict:
        """Check if a sample complies with environmental standards."""
        if sample_id not in self.env_samples:
            return {"error": "Sample ID not found"}

        sample = self.env_samples[sample_id]
        compliance_status = {}

        for parameter, value in sample["parameters"].items():
            if value is None:
                compliance_status[parameter] = {"status": "Not Tested", "value": None}
                continue

            standard = self.water_standards.get(parameter)
            if not standard:
                compliance_status[parameter] = {"status": "No Standard", "value": value}
                continue

            unit = standard.get("unit", "")
            max_allowed = standard.get("max_allowed")
            min_allowed = standard.get("min_allowed")

            if min_allowed is not None and max_allowed is not None:
                if min_allowed <= value <= max_allowed:
                    compliance_status[parameter] = {"status": "Compliant", "value": value, "unit": unit}
                else:
                    compliance_status[parameter] = {"status": "Non-Compliant", "value": value, "unit": unit, "limit": f"{min_allowed}-{max_allowed} {unit}"}
            elif max_allowed is not None:
                if value <= max_allowed:
                    compliance_status[parameter] = {"status": "Compliant", "value": value, "unit": unit}
                else:
                    compliance_status[parameter] = {"status": "Non-Compliant", "value": value, "unit": unit, "limit": f"≤ {max_allowed} {unit}"}

        return compliance_status

    def generate_compliance_report(self, sample_ids: List[str]) -> str:
        """Generate a compliance report for multiple samples."""
        report_id = f"REP{self.next_report_id}"
        compliance_data = {}

        for sample_id in sample_ids:
            if sample_id in self.env_samples:
                compliance_data[sample_id] = self.check_compliance(sample_id)

        self.compliance_reports[report_id] = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "samples": sample_ids,
            "compliance_status": compliance_data,
            "notes": "Generated automatically"
        }
        self.next_report_id += 1
        return f"Compliance report generated with ID: {report_id}"

    # --- Lab Equipment Management ---
    def add_equipment(self, name: str, equipment_type: str) -> str:
        """Add a new piece of lab equipment."""
        equipment_id = f"EQ{self.next_equipment_id}"
        self.lab_equipment[equipment_id] = {
            "name": name,
            "type": equipment_type,
            "status": "Available",
            "last_calibration": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        self.next_equipment_id += 1
        return f"Equipment '{name}' added with ID: {equipment_id}"

    def calibrate_equipment(self, equipment_id: str) -> str:
        """Calibrate a piece of lab equipment."""
        if equipment_id in self.lab_equipment:
            self.lab_equipment[equipment_id]["last_calibration"] = datetime.datetime.now().strftime("%Y-%m-%d")
            self.lab_equipment[equipment_id]["status"] = "Calibrated"
            return f"Equipment {equipment_id} calibrated."
        return f"Equipment ID {equipment_id} not found."

    # --- Helper Methods ---
    def get_eia_report(self, eia_id: str) -> Optional[Dict]:
        """Retrieve an EIA report by ID."""
        return self.eia_reports.get(eia_id)

    def get_sample(self, sample_id: str) -> Optional[Dict]:
        """Retrieve a sample by ID."""
        return self.env_samples.get(sample_id)

    def get_compliance_report(self, report_id: str) -> Optional[Dict]:
        """Retrieve a compliance report by ID."""
        return self.compliance_reports.get(report_id)

# --- Example Usage ---
if __name__ == "__main__":
    lab = EnvironmentalLabAnalyst()

    # Conduct an Environmental Impact Assessment (EIA)
    print("=== Environmental Impact Assessment (EIA) ===")
    print(lab.create_eia("River Nile Delta", ["Water Pollution", "Habitat Loss", "Soil Erosion"]))
    print(lab.add_mitigation_measure("EIA1", "Water Pollution", "Install water treatment plants"))
    print(lab.add_mitigation_measure("EIA1", "Habitat Loss", "Create protected zones"))
    print(lab.finalize_eia("EIA1"))

    # Collect and analyze environmental samples
    print("\n=== Sample Collection and Analysis ===")
    print(lab.collect_sample("Water", "River Nile, Site A", ["dissolved_oxygen", "chlorine", "lead", "pH"]))
    print(lab.measure_dissolved_oxygen("SAMP1", 4.5))
    print(lab.measure_chlorine("SAMP1", 3.2))
    print(lab.measure_heavy_metal("SAMP1", "lead", 8.0))

    # Check compliance with environmental standards
    print("\n=== Compliance Checks ===")
    compliance = lab.check_compliance("SAMP1")
    for param, status in compliance.items():
        print(f"{param}: {status}")

    # Generate a compliance report
    print("\n=== Compliance Report ===")
    print(lab.generate_compliance_report(["SAMP1"]))

    # Manage lab equipment
    print("\n=== Lab Equipment Management ===")
    print(lab.add_equipment("DO Meter", "Water Quality Analyzer"))
    print(lab.add_equipment("Spectrophotometer", "Heavy Metal Analyzer"))
    print(lab.calibrate_equipment("EQ1"))

    # Retrieve and display reports
    print("\n=== Retrieved Reports ===")
    print("EIA Report:", lab.get_eia_report("EIA1"))
    print("Sample Data:", lab.get_sample("SAMP1"))
    print("Compliance Report:", lab.get_compliance_report("REP1"))
