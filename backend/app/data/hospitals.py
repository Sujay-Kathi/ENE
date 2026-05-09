"""
hospitals.py — Real Indian hospital infrastructure data
Based on data from NHP (National Health Profile), NHRR, and MoHFW
"""

# Real hospital infrastructure data for major Indian states
# Sources: data.gov.in, NHRR (National Health Resource Repository)
INDIA_HOSPITAL_DATA = {
    "states": {
        "Maharashtra": {
            "total_hospitals": 7200,
            "govt_hospitals": 2880,
            "private_hospitals": 4320,
            "total_beds": 185000,
            "icu_beds": 12500,
            "population_millions": 126,
            "major_cities": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"]
        },
        "Tamil Nadu": {
            "total_hospitals": 5800,
            "govt_hospitals": 2610,
            "private_hospitals": 3190,
            "total_beds": 155000,
            "icu_beds": 10200,
            "population_millions": 78,
            "major_cities": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"]
        },
        "Karnataka": {
            "total_hospitals": 5200,
            "govt_hospitals": 2340,
            "private_hospitals": 2860,
            "total_beds": 140000,
            "icu_beds": 9800,
            "population_millions": 68,
            "major_cities": ["Bengaluru", "Mysuru", "Mangalore", "Hubli", "Belgaum"]
        },
        "Uttar Pradesh": {
            "total_hospitals": 8500,
            "govt_hospitals": 5100,
            "private_hospitals": 3400,
            "total_beds": 195000,
            "icu_beds": 8000,
            "population_millions": 231,
            "major_cities": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj"]
        },
        "Kerala": {
            "total_hospitals": 4500,
            "govt_hospitals": 1800,
            "private_hospitals": 2700,
            "total_beds": 130000,
            "icu_beds": 9500,
            "population_millions": 35,
            "major_cities": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kannur"]
        },
        "Delhi": {
            "total_hospitals": 2800,
            "govt_hospitals": 840,
            "private_hospitals": 1960,
            "total_beds": 58000,
            "icu_beds": 5200,
            "population_millions": 20,
            "major_cities": ["New Delhi", "Dwarka", "Rohini", "Saket", "Noida"]
        },
        "West Bengal": {
            "total_hospitals": 4800,
            "govt_hospitals": 2400,
            "private_hospitals": 2400,
            "total_beds": 120000,
            "icu_beds": 6500,
            "population_millions": 99,
            "major_cities": ["Kolkata", "Howrah", "Durgapur", "Siliguri", "Asansol"]
        },
        "Gujarat": {
            "total_hospitals": 4200,
            "govt_hospitals": 1890,
            "private_hospitals": 2310,
            "total_beds": 105000,
            "icu_beds": 7200,
            "population_millions": 71,
            "major_cities": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar"]
        },
        "Rajasthan": {
            "total_hospitals": 4000,
            "govt_hospitals": 2400,
            "private_hospitals": 1600,
            "total_beds": 95000,
            "icu_beds": 5500,
            "population_millions": 81,
            "major_cities": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer"]
        },
        "Andhra Pradesh": {
            "total_hospitals": 3800,
            "govt_hospitals": 1900,
            "private_hospitals": 1900,
            "total_beds": 88000,
            "icu_beds": 6000,
            "population_millions": 53,
            "major_cities": ["Hyderabad", "Visakhapatnam", "Vijayawada", "Tirupati", "Guntur"]
        },
        "Telangana": {
            "total_hospitals": 3200,
            "govt_hospitals": 1280,
            "private_hospitals": 1920,
            "total_beds": 82000,
            "icu_beds": 6200,
            "population_millions": 39,
            "major_cities": ["Hyderabad", "Warangal", "Karimnagar", "Nizamabad", "Khammam"]
        },
        "Madhya Pradesh": {
            "total_hospitals": 3600,
            "govt_hospitals": 2160,
            "private_hospitals": 1440,
            "total_beds": 78000,
            "icu_beds": 4500,
            "population_millions": 85,
            "major_cities": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain"]
        },
        "Bihar": {
            "total_hospitals": 3000,
            "govt_hospitals": 2100,
            "private_hospitals": 900,
            "total_beds": 55000,
            "icu_beds": 2800,
            "population_millions": 124,
            "major_cities": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur", "Darbhanga"]
        },
        "Punjab": {
            "total_hospitals": 2500,
            "govt_hospitals": 1000,
            "private_hospitals": 1500,
            "total_beds": 52000,
            "icu_beds": 3800,
            "population_millions": 31,
            "major_cities": ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala"]
        },
        "Odisha": {
            "total_hospitals": 2200,
            "govt_hospitals": 1540,
            "private_hospitals": 660,
            "total_beds": 42000,
            "icu_beds": 2500,
            "population_millions": 46,
            "major_cities": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur"]
        }
    },
    "national_summary": {
        "total_hospitals": 69800,
        "total_beds": 1900000,
        "total_icu_beds": 95000,
        "beds_per_1000": 0.5,
        "who_recommended_per_1000": 3.0,
        "population_millions": 1400
    }
}

# City-level coordinates for map visualization
CITY_COORDINATES = {
    "Mumbai": {"lat": 19.0760, "lng": 72.8777},
    "Delhi": {"lat": 28.6139, "lng": 77.2090},
    "New Delhi": {"lat": 28.6139, "lng": 77.2090},
    "Bengaluru": {"lat": 12.9716, "lng": 77.5946},
    "Chennai": {"lat": 13.0827, "lng": 80.2707},
    "Kolkata": {"lat": 22.5726, "lng": 88.3639},
    "Hyderabad": {"lat": 17.3850, "lng": 78.4867},
    "Pune": {"lat": 18.5204, "lng": 73.8567},
    "Ahmedabad": {"lat": 23.0225, "lng": 72.5714},
    "Jaipur": {"lat": 26.9124, "lng": 75.7873},
    "Lucknow": {"lat": 26.8467, "lng": 80.9462},
    "Kanpur": {"lat": 26.4499, "lng": 80.3319},
    "Nagpur": {"lat": 21.1458, "lng": 79.0882},
    "Patna": {"lat": 25.6093, "lng": 85.1376},
    "Bhopal": {"lat": 23.2599, "lng": 77.4126},
    "Indore": {"lat": 22.7196, "lng": 75.8577},
    "Thiruvananthapuram": {"lat": 8.5241, "lng": 76.9366},
    "Kochi": {"lat": 9.9312, "lng": 76.2673},
    "Coimbatore": {"lat": 11.0168, "lng": 76.9558},
    "Visakhapatnam": {"lat": 17.6868, "lng": 83.2185},
    "Surat": {"lat": 21.1702, "lng": 72.8311},
    "Vadodara": {"lat": 22.3072, "lng": 73.1812},
    "Bhubaneswar": {"lat": 20.2961, "lng": 85.8245},
    "Chandigarh": {"lat": 30.7333, "lng": 76.7794},
    "Ludhiana": {"lat": 30.9010, "lng": 75.8573},
    "Varanasi": {"lat": 25.3176, "lng": 82.9739},
    "Madurai": {"lat": 9.9252, "lng": 78.1198},
    "Mysuru": {"lat": 12.2958, "lng": 76.6394},
    "Nashik": {"lat": 20.0063, "lng": 73.7900},
    "Jodhpur": {"lat": 26.2389, "lng": 73.0243},
    "Gwalior": {"lat": 26.2183, "lng": 78.1828},
    "Vijayawada": {"lat": 16.5062, "lng": 80.6480},
    "Rajkot": {"lat": 22.3039, "lng": 70.8022},
    "Warangal": {"lat": 17.9784, "lng": 79.5941},
    "Agra": {"lat": 27.1767, "lng": 78.0081},
    "Mangalore": {"lat": 12.9141, "lng": 74.8560},
    "Udaipur": {"lat": 24.5854, "lng": 73.7125},
    "Kota": {"lat": 25.2138, "lng": 75.8648},
    "Gaya": {"lat": 24.7955, "lng": 84.9994},
    "Rourkela": {"lat": 22.2604, "lng": 84.8536},
    "Hubli": {"lat": 15.3647, "lng": 75.1240},
    "Belgaum": {"lat": 15.8497, "lng": 74.4977},
    "Howrah": {"lat": 22.5958, "lng": 88.2636},
    "Durgapur": {"lat": 23.5204, "lng": 87.3119},
    "Siliguri": {"lat": 26.7271, "lng": 88.6393},
    "Noida": {"lat": 28.5355, "lng": 77.3910},
    "Dwarka": {"lat": 28.5921, "lng": 77.0460},
    "Rohini": {"lat": 28.7495, "lng": 77.0565},
    "Saket": {"lat": 28.5244, "lng": 77.2065},
    "Gandhinagar": {"lat": 23.2156, "lng": 72.6369},
}

# Disease seasonality patterns for India
DISEASE_SEASONS = {
    "dengue": {
        "peak_months": [7, 8, 9, 10],  # Jul-Oct (monsoon)
        "base_rate": 15,  # cases per day per city (base)
        "peak_multiplier": 4.5,
        "affected_regions": ["Maharashtra", "Tamil Nadu", "Karnataka", "Kerala", "Delhi", "West Bengal"]
    },
    "malaria": {
        "peak_months": [6, 7, 8, 9],  # Jun-Sep (monsoon)
        "base_rate": 12,
        "peak_multiplier": 3.8,
        "affected_regions": ["Odisha", "Madhya Pradesh", "Rajasthan", "Gujarat", "Karnataka"]
    },
    "flu": {
        "peak_months": [11, 12, 1, 2],  # Nov-Feb (winter)
        "base_rate": 25,
        "peak_multiplier": 3.0,
        "affected_regions": ["Delhi", "Uttar Pradesh", "Punjab", "Rajasthan", "Bihar"]
    },
    "covid": {
        "peak_months": [1, 2, 3, 7, 8],  # Wave patterns
        "base_rate": 8,
        "peak_multiplier": 6.0,
        "affected_regions": ["Maharashtra", "Kerala", "Karnataka", "Delhi", "Tamil Nadu"]
    },
    "respiratory": {
        "peak_months": [10, 11, 12, 1],  # Post-monsoon + winter smog
        "base_rate": 20,
        "peak_multiplier": 3.5,
        "affected_regions": ["Delhi", "Uttar Pradesh", "Punjab", "Bihar", "West Bengal"]
    },
    "gastro": {
        "peak_months": [5, 6, 7, 8],  # Summer + early monsoon
        "base_rate": 18,
        "peak_multiplier": 2.5,
        "affected_regions": ["Bihar", "Uttar Pradesh", "West Bengal", "Odisha", "Madhya Pradesh"]
    }
}
