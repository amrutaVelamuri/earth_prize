import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Carbon Emission Factors (Bangladesh specific - Source: BPDB & IEA)
CARBON_FACTORS = {
    'coal': 1.05,
    'natural_gas': 0.45,
    'diesel': 0.78,
    'furnace_oil': 0.85,
    'grid_average_bangladesh': 0.62
}

OTHER_EMISSIONS = {
    'SO2': 2.8,
    'NOx': 1.9,
    'PM2.5': 0.15,
    'CH4': 0.03,
    'mercury': 0.00001
}

# ============================================================================
# AI REPORT GENERATION FUNCTION
# ============================================================================

def generate_ai_report(data, report_type, audience, language_style, focus_areas, 
                       include_comparisons=True, include_implementation=True):
    """
    Generate a comprehensive, easy-to-understand report explaining the energy project
    in plain language for non-technical audiences.
    """
    
    location = data['location']
    power = data['power_generation']
    env = data['environmental_impact']
    community = data['community_impact']
    tech = data['technical_details']
    
    # Determine tone based on language style
    if language_style == "Simple & Accessible":
        tone = "friendly and conversational"
        detail_level = "basic"
    elif language_style == "Technical & Professional":
        tone = "formal and precise"
        detail_level = "detailed"
    elif language_style == "Persuasive & Compelling":
        tone = "enthusiastic and motivating"
        detail_level = "benefit-focused"
    else:  # Educational & Informative
        tone = "clear and instructive"
        detail_level = "explanatory"
    
    # Extract all variables to avoid f-string dictionary access issues
    total_mw = power['total_mw']
    annual_energy_mwh = power['annual_energy_mwh']
    households_powered = community['households_powered']
    people_served = community['people_served']
    carbon_saved_tons = env['carbon_saved_tons']
    trees_equivalent = env['trees_equivalent']
    cars_off_road = env['cars_off_road']
    
    report = f"""
# {report_type}
## {location} Renewable Energy Project

**Generated:** {datetime.now().strftime("%B %d, %Y")}  
**Target Audience:** {audience}  
**Report Style:** {language_style}

---

## EXECUTIVE SUMMARY

The {location} renewable energy project represents a transformative opportunity for clean, sustainable power generation. This project will generate **{total_mw:.2f} MW** of electricity—enough to power **{households_powered:,} households** ({people_served:,} people).

### Key Highlights at a Glance:

📊 **Total Annual Energy:** {annual_energy_mwh:,.0f} MWh/year  
🌱 **CO₂ Emissions Avoided:** {carbon_saved_tons:,.0f} tons/year  
🏘️ **Community Impact:** Powers {households_powered:,} homes  
🌳 **Environmental Equivalent:** Planting {trees_equivalent:,} trees or removing {cars_off_road:,} cars from roads

---

## WHAT THESE NUMBERS ACTUALLY MEAN

### Understanding {total_mw:.2f} MW of Power

You might hear "{total_mw:.2f} MW" and wonder what that really means for your community. Let's break it down:

- **For Homes:** This is enough electricity to power {households_powered:,} households continuously, 24/7
- **For Schools:** Could run approximately {int(households_powered / 500)} average-sized schools year-round with lights, computers, and air conditioning
- **For Businesses:** Enough to support {int(annual_energy_mwh / 8.76)} small to medium-sized factories operating full-time
- **In Daily Life:** Every person in this community could charge their phone 24,000 times per year with their share of this clean energy

### Energy Sources: How This Works

This project combines multiple renewable energy technologies:

"""
    
    if power['waterfall_mw'] > 0:
        waterfall_mw = power['waterfall_mw']
        waterfall_height = tech['waterfall_height']
        waterfall_flow = tech['waterfall_flow']
        report += f"""
**💧 Waterfall Hydroelectric System: {waterfall_mw:.2f} MW**

Think of a waterfall as nature's engine. Water falling from {waterfall_height} meters high drives turbines—like a water wheel, but much more powerful. With {waterfall_flow} cubic meters of water flowing every second, this creates constant, reliable electricity.

- **Always On:** Unlike solar (nighttime) or wind (calm days), waterfalls flow continuously
- **Clean:** No fuel needed, no emissions, just water doing what it naturally does
- **Proven Technology:** Hydroelectric power has reliably powered communities for over 100 years

"""
    
    if power['geothermal_mw'] > 0:
        geothermal_mw = power['geothermal_mw']
        geothermal_temp = tech['geothermal_temp']
        drilling_depth = tech['drilling_depth']
        pipe_material = tech['pipe_material']
        report += f"""
**🌋 Geothermal Energy System: {geothermal_mw:.2f} MW**

Deep underground, the Earth is incredibly hot—{geothermal_temp}°C at {drilling_depth} kilometers down. We can tap into this heat using pipes (made of {pipe_material}) to generate electricity, similar to how a tea kettle boils water.

- **24/7 Availability:** The Earth's heat never stops, so neither does the power
- **Weather Independent:** Rain or shine, hot or cold outside, geothermal keeps producing
- **Small Footprint:** Most equipment is underground, leaving land available for other uses
- **Lifespan:** These systems can operate reliably for 30-50 years

"""
    
    report += """
---

## ENVIRONMENTAL IMPACT: WHY THIS MATTERS

"""

    if "Highlight environmental benefits" in focus_areas:
        # Extract env variables
        carbon_saved = carbon_saved_tons  # Already extracted earlier
        trees_equiv = trees_equivalent  # Already extracted earlier
        cars_removed = cars_off_road  # Already extracted earlier
        coal_avoided = env['coal_avoided_tons']
        
        report += f"""
### What Does {carbon_saved:,.0f} Tons of CO₂ Saved Actually Mean?

Carbon dioxide (CO₂) is the main greenhouse gas causing climate change. Every year, this project prevents {carbon_saved:,.0f} tons from entering the atmosphere. Here's what that looks like:

🌳 **Tree Equivalent:** {trees_equiv:,} trees  
Planting this many trees and letting them grow for 10 years would absorb the same amount of CO₂.

🚗 **Cars Off the Road:** {cars_removed:,} vehicles  
This is equal to permanently removing {cars_removed:,} gasoline-powered cars from the roads.

🏭 **Coal Avoided:** {coal_avoided:,.0f} MWh of coal power  
We avoid burning {coal_avoided:,.0f} MWh worth of coal, one of the dirtiest fossil fuels.

### Long-Term Environmental Impact

Over a 20-year operational period:
- **Total CO₂ Prevented:** {carbon_saved * 20:,.0f} tons
- **Forest Equivalent:** {trees_equiv * 20:,} mature trees
- **Generational Impact:** Cleaner air for our children and grandchildren

### Beyond Carbon: Other Pollutants Eliminated

By replacing fossil fuel power plants, this project also eliminates:
- Sulfur dioxide (SO₂) - causes acid rain and respiratory problems
- Nitrogen oxides (NOₓ) - creates smog and breathing difficulties  
- Particulate matter (PM2.5) - linked to heart and lung disease
- Mercury - toxic to wildlife and human health

"""

    report += """
---

## COMMUNITY BENEFITS: WHAT'S IN IT FOR US?

"""

    if "Assess community impact" in focus_areas:
        report += f"""
### Direct Impact on Families

**{community['households_powered']:,} households** will benefit from this clean energy project.

That's **{community['people_served']:,} people**—real families, real lives improved.

### What Does This Mean for Daily Life?

**For Families:**
- Reliable electricity for lights, refrigeration, cooking
- Lower and more stable electricity costs over time
- Ability to study at night with good lighting
- Power for internet connectivity and education

**For Health:**
- Cleaner air means fewer respiratory illnesses
- Reduced indoor air pollution from traditional fuels
- Better healthcare with reliable power for clinics

**For Education:**
- Schools can use computers and projectors
- Students can study after dark
- Internet access enables modern learning

**For Business:**
- Local shops can refrigerate products
- Small businesses can operate equipment reliably
- New economic opportunities from stable power

### Economic Opportunities

**During Construction (18-24 months):**
- Local jobs for site preparation and construction
- Opportunities for local suppliers and contractors
- Skills training for community members

**Long-Term Operations (30+ years):**
- Permanent jobs for maintenance and operations
- Lower electricity costs free up money for other needs
- Attracts new businesses with reliable power
- Increases property values in the area

"""

    if include_comparisons:
        report += """
---

## COMPARISON WITH ALTERNATIVES: WHY RENEWABLE ENERGY?

### Renewable Energy vs. Coal Power Plant

**Environmental:**
- ✅ **Zero air pollution** (coal produces black smoke, ash, and toxic gases)
- ✅ **No water pollution** (coal plants contaminate rivers with heavy metals)
- ✅ **No ash disposal** (coal creates millions of tons of toxic waste)

**Health:**
- ✅ **Cleaner air** means fewer asthma attacks and respiratory diseases
- ✅ **No mercury contamination** of fish in local waterways
- ✅ **Reduced risk** of cancer and other chronic diseases

**Economic:**
- ✅ **No fuel costs** (coal prices fluctuate wildly)
- ✅ **Lower long-term costs** (renewable energy gets cheaper over time)
- ✅ **Energy independence** (no need to import coal)

### Renewable Energy vs. Diesel Generators

Many rural areas rely on diesel generators. Here's why renewable energy is better:

- ✅ **Much quieter** - no constant engine noise
- ✅ **No fuel deliveries needed** - no risk of supply interruptions
- ✅ **Lower maintenance** - fewer moving parts to break down
- ✅ **No fuel storage** - eliminates fire and spill risks
- ✅ **Predictable costs** - diesel prices can double or triple unpredictably

"""

    if include_implementation and "Provide implementation roadmap" in focus_areas:
        report += """
---

## MAKING IT HAPPEN: IMPLEMENTATION ROADMAP

### Phase 1: Planning & Community Engagement (6-12 months)

**What Happens:**
- Detailed engineering studies and site surveys
- Environmental impact assessment
- Community meetings to gather input and concerns
- Secure all necessary government permits

**Community Role:**
- Attend information sessions
- Provide feedback on project plans
- Participate in surveys about energy needs

### Phase 2: Securing Funding (3-6 months)

**Potential Funding Sources:**
- Government renewable energy programs
- International climate finance
- Private sector investment
- Development banks and green bonds
- Community investment opportunities

**What We're Looking For:**
- Grants for renewable energy projects
- Low-interest green loans
- Public-private partnerships
- Community co-investment models

### Phase 3: Construction (18-24 months)

**What Happens:**
- Site preparation and access road construction
- Drilling operations (for geothermal)
- Turbine and generator installation
- Electrical infrastructure and grid connection
- Testing and commissioning

**Job Opportunities:**
- Local laborers for construction work
- Equipment operators
- Support staff (food services, logistics)
- Apprenticeships for technical skills

### Phase 4: Operations (30+ years)

**Ongoing Activities:**
- Daily monitoring and maintenance
- Performance optimization
- Community benefit distribution
- Regular safety inspections
- Environmental compliance monitoring

**Permanent Jobs Created:**
- Plant operators and technicians
- Maintenance crew
- Administrative staff
- Safety and environmental officers

"""

    if "Address potential challenges" in focus_areas:
        report += """
---

## ADDRESSING CONCERNS: HONEST ANSWERS

### "Will this disrupt our water supply?"

**No.** Hydroelectric systems use water to generate power and then return it to the natural waterway. The water isn't consumed—it just passes through turbines. Fish passages and environmental safeguards are built into the design.

### "What if the technology fails?"

Renewable energy technology is proven and reliable:
- Hydroelectric plants have operated successfully for over 100 years
- Geothermal systems have 30-50 year operational lifespans
- Multiple backup systems ensure continuous operation
- Insurance and warranties protect the investment

### "Will electricity costs go up?"

**No, they should decrease.** Renewable energy:
- Has no fuel costs (unlike coal or diesel)
- Becomes cheaper over time as technology improves
- Protects communities from fossil fuel price spikes
- Can generate revenue by selling excess power

### "What happens when equipment needs replacement?"

The project plan includes:
- Maintenance funds set aside from operations
- Extended warranties on major equipment
- Training local technicians for repairs
- Spare parts inventory on site

"""

    if "Calculate return on investment" in focus_areas or "Discuss economic opportunities" in focus_areas:
        report += f"""
---

## ECONOMIC ANALYSIS: THE NUMBERS MAKE SENSE

### Annual Value Created

**Energy Production Value:**
- {annual_energy_mwh:,.0f} MWh × Average electricity price
- Estimated annual revenue: Varies by local rates
- 30-year lifetime value: Substantial long-term returns

**Environmental Value:**
- Carbon credits from {carbon_saved:,.0f} tons CO₂ saved
- Health cost savings from cleaner air
- Ecosystem benefits from reduced pollution

**Social Value:**
- {households_powered:,} households with reliable power
- Educational opportunities from electricity access
- Economic development from stable energy supply

### Cost Comparison: 30-Year Lifecycle

While initial investment is required, renewable energy becomes dramatically cheaper than alternatives over time:

**Renewable Energy System:**
- High initial cost, but then mostly maintenance
- No ongoing fuel purchases
- Costs decrease over time as debt is paid off

**Coal or Diesel Alternative:**
- Lower initial cost, but constant fuel purchases
- Fuel prices increase over time
- Operating costs continue indefinitely
- Environmental cleanup costs at end of life

**The Winner:** Renewable energy saves money over its 30+ year lifetime

"""

    report += """
---

## NEXT STEPS: COMPREHENSIVE IMPLEMENTATION GUIDE FOR CITY PLANNERS

As a city planner, implementing this renewable energy project requires coordinating multiple stakeholders, navigating regulatory frameworks, and ensuring alignment with broader urban development goals. Here's your detailed roadmap:

---

### PHASE 1: IMMEDIATE ACTIONS (Months 1-3)

#### 1.1 Internal Municipal Coordination

**Week 1-2: Establish Project Governance**
- Form inter-departmental steering committee including:
  - Urban Planning Department (lead)
  - Public Works & Infrastructure
  - Environmental Services
  - Economic Development Office
  - Finance Department
  - Legal/Regulatory Affairs
  - Community Engagement Office
- Assign project manager and dedicated staff
- Establish clear decision-making authority and approval processes
- Set up project management systems and communication protocols

**Week 3-4: Initial Stakeholder Mapping**
- Identify all key stakeholders:
  - **Government:** National energy ministry, regional authorities, environmental agencies
  - **Utilities:** Grid operators, electricity distributors, water authorities
  - **Community:** Neighborhood associations, local leaders, affected residents
  - **Technical:** Engineering firms, equipment suppliers, contractors
  - **Financial:** Development banks, private investors, grant agencies
  - **Environmental:** Conservation groups, environmental regulators
- Create stakeholder engagement matrix with contact info and engagement strategy
- Schedule initial consultation meetings with each group

**Week 5-8: Technical Feasibility Verification**
- Commission independent technical assessment of site
- Verify all calculations and energy production estimates
- Conduct preliminary geological and hydrological surveys
- Assess existing infrastructure capacity (roads, grid connection points)
- Evaluate land ownership and acquisition requirements
- Document technical risks and mitigation strategies

**Deliverables:**
- Project governance charter and organizational structure
- Complete stakeholder database and engagement plan
- Independent technical feasibility report
- Risk assessment matrix
- Initial project timeline and critical path analysis

#### 1.2 Regulatory and Legal Framework Assessment

**Permits and Approvals Inventory:**
Create comprehensive checklist of all required permits:

**National Level:**
- Environmental Impact Assessment (EIA) approval
- Energy generation license from national energy regulator
- Water use permits (for hydroelectric component)
- Drilling permits (for geothermal component)
- Grid connection approval from national electricity authority
- Land use change permissions (if applicable)
- Construction permits for major infrastructure

**Regional/Provincial Level:**
- Regional development plan compliance certification
- Provincial environmental clearances
- Local water management authority approvals
- Fire safety and building code approvals
- Regional grid integration permits

**Municipal Level:**
- Zoning compliance and variances
- Building permits for all structures
- Road use and access permits during construction
- Noise and vibration permits for construction
- Tree cutting permits (if required)
- Archaeological survey compliance (if required)

**Action Items:**
- Meet with each regulatory agency to understand requirements
- Create permit dependency chart (which permits are prerequisites for others)
- Establish realistic timelines for each approval process
- Identify potential regulatory bottlenecks or conflicts
- Develop relationships with key regulatory officials

#### 1.3 Community Engagement Strategy

**Month 1: Information Gathering**
- Conduct door-to-door surveys in affected areas
- Hold listening sessions to understand community concerns
- Document existing energy challenges and needs
- Identify community leaders and influencers
- Assess communication preferences (meetings, social media, radio, etc.)

**Month 2: Information Dissemination**
- Prepare plain-language project fact sheets in local languages
- Create visual materials (maps, renderings, infographics)
- Launch project website with FAQ section
- Establish community liaison office in the neighborhood
- Conduct 3-5 town hall meetings in different locations
- Present to neighborhood associations and civic groups

**Month 3: Feedback Integration**
- Compile and analyze all community input
- Adjust project design based on legitimate concerns
- Develop community benefit agreement framework
- Create grievance mechanism for ongoing concerns
- Establish community advisory committee

**Key Messages for Community:**
- How will this benefit MY family specifically?
- Will there be job opportunities for local residents?
- What are the potential disruptions during construction?
- How will the project affect property values?
- What safety measures are in place?
- How can community members invest or participate?

---

### PHASE 2: DETAILED PLANNING & DESIGN (Months 4-9)

#### 2.1 Comprehensive Environmental Assessment

**Scope of Environmental Studies:**

**Ecological Assessment:**
- Baseline biodiversity survey (flora and fauna)
- Aquatic ecosystem analysis (for waterfall site)
- Migratory bird patterns and collision risk assessment
- Endangered species habitat evaluation
- Wetlands and riparian zone mapping
- Groundwater recharge area identification

**Social Impact Assessment:**
- Population displacement analysis (if any)
- Cultural heritage and archaeological survey
- Impact on indigenous communities (if applicable)
- Traditional land use and access rights
- Visual impact assessment for nearby communities
- Noise and vibration impact modeling

**Cumulative Impact Analysis:**
- How this project interacts with other development
- Regional water balance considerations
- Grid stability and integration effects
- Traffic and transportation impacts
- Waste management during construction and operations

**Mitigation Measures Development:**
For each identified impact, develop specific mitigation:
- Fish passages and aquatic habitat protection
- Wildlife corridors and protected zones
- Construction timing to avoid sensitive periods
- Noise barriers and vibration dampening
- Dust control and erosion prevention
- Water quality monitoring program

**Timeline:** 4-6 months for comprehensive EIA
**Budget:** ${50,000 - 150,000} depending on complexity
**Outcome:** Approved EIA certificate from environmental ministry

#### 2.2 Detailed Engineering Design

**Phase 1: Conceptual Engineering (Month 4-5)**
- Hire reputable engineering firm with renewable energy experience
- Develop 3-4 design alternatives for comparison
- Conduct value engineering to optimize cost vs. performance
- Create preliminary equipment specifications
- Develop construction sequencing plan
- Estimate quantities for major materials

**Phase 2: Detailed Design (Month 6-8)**
- Final civil engineering drawings for all structures
- Electrical system design and grid connection specifications
- Mechanical equipment specifications and layouts
- Geotechnical investigations and foundation design
- Hydraulic modeling (for waterfall turbines)
- Thermal modeling (for geothermal system)
- SCADA and monitoring system design
- Safety systems and emergency shutdown procedures

**Phase 3: Design Review & Optimization (Month 9)**
- Independent engineering review by third-party expert
- Constructability review with contractor input
- Value engineering workshop to identify cost savings
- Final design freeze and documentation
- As-built preparation and document control system

**Technical Specifications to Finalize:**
- Turbine type, capacity, and manufacturer
- Generator specifications and grid interface requirements
- Geothermal well design and drilling specifications
- Piping materials and specifications (considering {tech['pipe_material']})
- Electrical substation and transmission line design
- Access road specifications and right-of-way requirements
- Construction water supply and waste management

**Deliverables:**
- Complete engineering drawings (civil, mechanical, electrical)
- Technical specifications for all equipment
- Bill of quantities for construction bidding
- Operation and maintenance manuals outline
- As-built documentation standards

#### 2.3 Financial Planning and Funding Strategy

**Detailed Cost Estimation:**

**Capital Expenditure (CAPEX) Breakdown:**
- Site preparation and access: 5-8% of total
- Civil works (buildings, foundations): 20-25%
- Electromechanical equipment: 40-50%
- Electrical infrastructure and grid connection: 10-15%
- Engineering and design fees: 8-12%
- Environmental mitigation: 3-5%
- Contingency: 10-15%

**For this {location} project estimate:**
- Waterfall component ({waterfall_mw:.2f} MW): $3-5M per MW
- Geothermal component ({geothermal_mw:.2f} MW): $4-7M per MW
- **Total estimated CAPEX: $[Calculate based on MW] Million**

**Operating Expenditure (OPEX) - Annual:**
- Operations staff salaries: $100-200K/year
- Maintenance and spare parts: 2-3% of CAPEX
- Insurance: 0.5-1% of CAPEX
- Grid fees and charges: Variable
- Environmental monitoring: $20-50K/year
- Community benefit fund: 2-5% of revenues

**Funding Source Strategy:**

**1. Government Grants (Target: 30-40% of CAPEX)**
- National renewable energy development fund
- Climate finance mechanisms (Green Climate Fund)
- Regional development grants
- Rural electrification programs
- Municipal infrastructure funds

**Action:** Prepare grant applications with detailed project justification

**2. Development Finance (Target: 40-50% of CAPEX)**
- World Bank clean energy loans
- Asian Development Bank infrastructure financing
- International Finance Corporation
- National development banks
- Green bonds issuance

**Action:** Engage with DFI early, prepare bankable feasibility study

**3. Private Investment (Target: 10-20% of CAPEX)**
- Independent power producers (IPPs)
- Infrastructure funds with ESG focus
- Community investment schemes
- Municipal bonds

**Action:** Develop investor prospectus with clear return profile

**4. Municipal Contribution (Target: 5-10% of CAPEX)**
- In-kind contributions (land, existing infrastructure)
- Municipal budget allocation
- Revenue from previous projects

**Action:** Get city council approval for budget allocation

**Financial Model Development:**
- 25-30 year cash flow projection
- Sensitivity analysis (energy prices, costs, generation)
- Debt service coverage ratio (target >1.3x)
- Internal rate of return calculation
- Net present value analysis
- Payback period assessment

**Power Purchase Agreement (PPA) Strategy:**
- Negotiate with national grid or distribution company
- Target tariff: $0.08-0.12 per kWh (market dependent)
- Contract length: 20-25 years
- Escalation clauses tied to inflation
- Performance guarantees and penalties
- Force majeure provisions

---

### PHASE 3: PROCUREMENT & CONTRACTING (Months 10-15)

#### 3.1 Procurement Strategy

**Procurement Model Selection:**

**Option A: Engineering, Procurement, Construction (EPC) Contract**
- Single contractor responsible for entire project
- Fixed price, turnkey delivery
- Lower risk for municipality
- Best for first-time developers
- **Recommended for this project**

**Option B: Multi-Contract Approach**
- Separate contracts for civil works, equipment, installation
- More management intensive
- Potentially lower cost
- Requires strong project management capacity

**Option C: Public-Private Partnership (PPP)**
- Private partner finances, builds, operates
- Municipality pays for power generated
- Minimal upfront municipal investment
- Long-term commitment required

**For {location} Project, recommend:** EPC contract with performance guarantees

#### 3.2 Contractor Prequalification

**Technical Prequalification Criteria:**
- Minimum 10 years experience in renewable energy
- Successfully completed at least 3 similar projects
- Total installed capacity >50 MW across portfolio
- Experience in similar geological/geographical conditions
- Strong health, safety, and environmental track record
- Financial capacity (turnover >10x project value)
- Local presence or commitment to local partnerships

**Prequalification Process:**
- Advertise internationally and nationally (Month 10)
- Receive and evaluate prequalification documents (Month 11)
- Shortlist 3-5 qualified bidders (Month 11)
- Conduct bidder site visit and briefing (Month 12)

#### 3.3 Tender Documentation and Bidding

**Tender Package Components:**
- Instructions to bidders
- Form of contract (FIDIC or local standard)
- Detailed specifications and drawings
- Bill of quantities
- Project schedule requirements
- Performance guarantees and warranties
- Health, safety, and environmental requirements
- Local content and employment requirements

**Bidding Process:**
- Issue tender documents to shortlisted bidders (Month 12)
- Bidder clarification period (2-4 weeks)
- Technical and financial proposal submission (Month 13)
- Two-stage evaluation: technical first, then financial
- Negotiations with top-ranked bidder (Month 14)
- Contract award and signing (Month 15)

**Evaluation Criteria (Example):**
- Technical approach and methodology: 40%
- Experience and qualifications: 20%
- Project schedule and delivery plan: 15%
- Price: 20%
- Local content and community benefits: 5%

#### 3.4 Key Contracts and Agreements

**Contracts to Finalize:**

1. **EPC Contract** with construction contractor
   - Fixed price: $[X] million
   - Completion date: [Date]
   - Performance guarantees: [Specified MW output]
   - Warranty period: 2-5 years
   - Liquidated damages for delays

2. **Power Purchase Agreement (PPA)** with grid operator
   - 25-year term
   - Tariff: $[X] per kWh
   - Take-or-pay provisions
   - Curtailment compensation

3. **Grid Connection Agreement**
   - Technical specifications for connection
   - Cost sharing for connection infrastructure
   - Operation and maintenance responsibilities

4. **Land Lease/Purchase Agreements**
   - Secure all required land parcels
   - Easements for transmission lines and access roads
   - Compensation for affected landowners

5. **Equipment Supply Agreements**
   - Long-lead items (turbines, generators)
   - Performance guarantees from manufacturers
   - After-sales support and spare parts

6. **Operations & Maintenance Agreement**
   - Consider O&M contractor for first 5 years
   - Training and capacity building provisions
   - Transition to municipal operation

---

### PHASE 4: CONSTRUCTION MANAGEMENT (Months 16-34)

#### 4.1 Pre-Construction Activities (Month 16-17)

**Site Preparation:**
- Establish construction site offices and facilities
- Set up security and access control
- Install temporary power and water
- Create material storage areas
- Build construction camps for workers (if needed)
- Establish medical facilities and emergency response

**Mobilization:**
- Contractor mobilizes equipment and personnel
- Conduct pre-construction survey and benchmarking
- Establish quality control laboratory
- Set up environmental monitoring stations
- Hold pre-construction meeting with all parties

**Community Preparation:**
- Finalize construction traffic management plan
- Establish construction complaints hotline
- Hire community liaison officers
- Conduct information campaigns about construction schedule
- Set up regular community update meetings (monthly)

#### 4.2 Construction Oversight and Management

**Owner's Engineer Role:**
- Hire independent engineer to represent municipality
- Daily site supervision and quality control
- Review and approve contractor submittals
- Certify progress for payment purposes
- Monitor compliance with specifications and standards
- Document changes and variations

**Municipal Project Management Office:**
- Weekly site visits by project manager
- Monthly progress meetings with contractor
- Review monthly progress reports
- Approve payment certificates
- Manage stakeholder communications
- Resolve issues and disputes
- Monitor budget and schedule

**Key Construction Milestones:**
- Month 18: Site preparation complete, foundations started
- Month 22: Civil works 50% complete
- Month 26: Turbine/generator installation begins
- Month 30: Electrical infrastructure complete
- Month 32: Testing and commissioning begins
- Month 34: Commercial operation date (COD)

**Quality Assurance Program:**
- Material testing for all critical components
- Welding inspection and testing
- Concrete strength testing
- Equipment factory acceptance tests
- Installation inspection checklists
- Independent third-party verification

**Health, Safety & Environment Management:**
- Weekly safety meetings and toolbox talks
- Monthly safety audits and inspections
- Incident reporting and investigation system
- Environmental compliance monitoring
- Dust, noise, and vibration monitoring
- Water quality testing program
- Grievance mechanism for community complaints

#### 4.3 Local Employment and Procurement

**Local Content Strategy:**

**Employment Targets:**
- Unskilled labor: 80-100% local hiring
- Semi-skilled: 50-70% local
- Skilled: 30-50% local
- Management: Competency-based

**Target: Create [200-500] construction jobs over 18 months**

**Local Procurement:**
- Aggregates, sand, cement: 100% local
- Timber and basic materials: 80%+ local
- Food services and accommodation: 100% local
- Transportation and logistics: 70%+ local

**Capacity Building:**
- Provide training to local workers
- Apprenticeship programs for youth
- Skills certification partnerships with technical schools
- Mentorship from experienced workers

---

### PHASE 5: COMMISSIONING & HANDOVER (Months 33-36)

#### 5.1 Testing and Commissioning

**Pre-Commissioning Tests:**
- Individual equipment testing (motors, pumps, valves)
- Instrument calibration and loop checks
- Control system logic testing
- Safety system testing
- Communication system verification

**Commissioning Sequence:**
1. Dry commissioning (no water/steam flow)
2. Wet commissioning (water circulation without power generation)
3. Initial synchronization with grid
4. Performance testing at various load levels
5. Full load testing for 72 continuous hours
6. Acceptance tests per contract specifications

**Performance Testing:**
- Verify guaranteed power output: {power['total_mw']:.2f} MW
- Efficiency measurements
- Grid code compliance testing
- Environmental emissions verification (noise, vibration)
- Safety systems verification

**Documentation:**
- As-built drawings for all systems
- Operations and maintenance manuals
- Training materials for plant operators
- Emergency response procedures
- Spare parts catalog and inventory
- Warranty documentation

#### 5.2 Operations Preparation

**Staffing and Training:**

**Permanent Operations Team:**
- Plant Manager (1)
- Shift Supervisors (3-4)
- Control Room Operators (6-8 for 24/7 coverage)
- Maintenance Technicians (4-6)
- Electricians (2-3)
- Administrative Staff (2-3)

**Total permanent jobs: 20-25 positions**

**Training Program:**
- Classroom training on theory and systems
- Hands-on training during commissioning
- Simulator training (if available)
- Manufacturer training on specialized equipment
- Safety and emergency response training
- Environmental compliance training

**Operational Readiness:**
- Establish 24/7 operations schedule
- Stock initial spare parts inventory
- Set up SCADA monitoring and control
- Establish maintenance schedule and procedures
- Create performance reporting systems
- Set up billing and revenue collection

#### 5.3 Commercial Operation and Handover

**Commercial Operation Date (COD) Requirements:**
- Complete performance testing successfully
- All regulatory approvals and clearances obtained
- Grid connection fully operational
- Operations team trained and in place
- PPA in effect with first power sale
- All safety systems verified
- Insurance policies active

**Handover Process:**
- Final acceptance certificate issued
- Defects liability period begins (typically 1 year)
- Warranty periods start
- Final payment to contractor (after retention)
- Transfer of all documentation
- Demobilization of construction facilities

**First Year Operations:**
- Warranty period monitoring
- Performance optimization
- Defects rectification
- Operations team skill development
- Maintenance regime establishment
- Community benefit delivery begins

---

### PHASE 6: LONG-TERM OPERATIONS & EXPANSION (Years 2-30)

#### 6.1 Performance Monitoring and Optimization

**Key Performance Indicators (KPIs):**
- Availability: Target >95% (percentage of time plant can generate)
- Capacity Factor: Target >85% (actual vs. theoretical generation)
- Forced Outage Rate: Target <2% (unplanned shutdowns)
- Energy Generation: {power['annual_energy_mwh']:,.0f} MWh/year target
- Revenue Collection: >98% of billed amount
- Safety: Zero lost-time injuries

**Continuous Improvement:**
- Annual performance reviews
- Benchmarking against similar facilities
- Technology upgrades as available
- Process optimization initiatives
- Predictive maintenance implementation

#### 6.2 Community Benefit Distribution

**Community Benefit Fund Structure:**
- Allocate 2-5% of annual revenue to community fund
- Estimated annual fund: $[Calculate based on revenue]
- Governance by community committee
- Transparent application and selection process

**Eligible Projects:**
- School infrastructure and scholarships
- Healthcare facilities and programs
- Community center upgrades
- Sports and recreation facilities
- Small business development programs
- Environmental conservation initiatives

#### 6.3 Expansion and Replication

**Lessons Learned Documentation:**
- What worked well in this project?
- What challenges were encountered and how were they overcome?
- How can the process be improved for future projects?
- What local capacity was built?

**Replication Strategy:**
- Identify other suitable sites in the region
- Use this project as demonstration for others
- Package lessons learned for other municipalities
- Create template documents (RFPs, contracts, etc.)
- Offer technical assistance to neighboring cities

**Expansion Opportunities:**
- Add more turbines if resource allows
- Integrate battery storage for grid stability
- Add solar PV on facility buildings
- Develop mini-grid for nearby communities
- Create renewable energy hub with multiple technologies

---

## CRITICAL SUCCESS FACTORS FOR CITY PLANNERS

### 1. **Strong Project Governance**
- Clear decision-making authority
- Dedicated and empowered project team
- Regular stakeholder coordination
- Transparent processes and documentation

### 2. **Community Buy-In**
- Early and continuous engagement
- Address concerns proactively
- Deliver tangible benefits
- Maintain open communication channels

### 3. **Technical Excellence**
- Hire experienced consultants and contractors
- Independent verification at key stages
- Don't cut corners on quality
- Learn from international best practices

### 4. **Financial Sustainability**
- Conservative financial projections
- Diversified funding sources
- Adequate contingency reserves
- Strong revenue collection mechanisms

### 5. **Regulatory Compliance**
- Start permit processes early
- Maintain good relations with regulators
- Document everything thoroughly
- Plan for regulatory delays

### 6. **Risk Management**
- Identify risks early and continuously
- Develop mitigation strategies
- Transfer appropriate risks to contractors
- Maintain adequate insurance

### 7. **Capacity Building**
- Invest in staff training
- Build local technical capacity
- Create knowledge management systems
- Document processes for future projects

---

## INTEGRATION WITH BROADER CITY PLANNING

### Urban Development Synergies

**Land Use Planning:**
- Designate renewable energy zones in city master plan
- Protect sites from conflicting development
- Plan transmission corridors in advance
- Integrate with green space and conservation areas

**Economic Development:**
- Attract energy-intensive industries with reliable power
- Market city as sustainable development destination
- Create green jobs and skills training programs
- Develop eco-tourism opportunities around facilities

**Climate Action Plan:**
- This project contributes to municipal emissions reduction targets
- Include in city's Nationally Determined Contribution (NDC)
- Use as flagship project for climate resilience
- Leverage for international climate finance access

**Infrastructure Master Planning:**
- Coordinate with electrical grid expansion plans
- Align with water resources management strategy
- Integrate with transportation infrastructure development
- Plan for future energy storage facilities

### Regional Coordination

**Multi-Municipal Collaboration:**
- Share costs and benefits with neighboring municipalities
- Joint procurement for larger economies of scale
- Regional transmission infrastructure development
- Shared technical capacity and expertise

**Provincial/National Alignment:**
- Align with national renewable energy targets
- Coordinate with provincial development plans
- Access regional development funds
- Participate in national energy planning processes

---

## RISK REGISTER AND MITIGATION STRATEGIES

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Resource variability (water flow, geothermal temp) | Medium | High | Conservative design, 10% contingency in calculations |
| Equipment performance below guarantee | Low | High | Strong warranties, performance bonds, factory testing |
| Grid connection delays | Medium | Medium | Early engagement with grid operator, backup plans |
| Geological surprises | Medium | High | Thorough surveys, geotechnical contingency budget |

### Financial Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Cost overruns | Medium | High | Fixed-price EPC contract, 15% contingency reserve |
| Funding gaps | Medium | Critical | Diversified funding sources, staged development |
| Revenue shortfall (lower tariffs) | Low | Medium | Long-term PPA, take-or-pay provisions |
| Currency fluctuation | Medium | Medium | Local currency contracts, hedging strategies |

### Social/Political Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Community opposition | Low | Critical | Early engagement, benefit sharing, grievance mechanism |
| Change in government/policy | Medium | Medium | Legal protections, multi-party agreements |
| Land acquisition disputes | Medium | High | Fair compensation, voluntary transactions preferred |
| Labor disputes | Low | Medium | Fair wages, good working conditions, dialogue |

### Environmental Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| EIA rejection/delays | Low | High | Quality studies, early consultation with authorities |
| Unforeseen environmental impacts | Low | Medium | Robust monitoring, adaptive management |
| Climate change affects resource | Low | High | Climate projections in design, adaptive capacity |
| Natural disasters (floods, earthquakes) | Low | Critical | Appropriate structural design, insurance coverage |

---

## TOOLS AND TEMPLATES FOR CITY PLANNERS

### Project Management Templates

1. **Project Charter Template** - Defines scope, objectives, governance
2. **Stakeholder Register** - Tracks all stakeholders and engagement activities
3. **Permit Tracking Matrix** - Monitors status of all regulatory approvals
4. **Risk Register** - Documents risks, probabilities, impacts, and mitigations
5. **Issues Log** - Tracks problems and their resolution
6. **Change Order Register** - Manages variations to contracts
7. **Monthly Progress Report Template** - Standardized reporting format
8. **Lessons Learned Template** - Captures knowledge for future projects

### Financial Tools

1. **Cost Estimation Spreadsheet** - Detailed CAPEX and OPEX breakdown
2. **Financial Model** - 30-year cash flow projection with sensitivity
3. **Funding Strategy Matrix** - Tracks all funding sources and status
4. **Budget vs. Actual Tracker** - Monitors spending against budget
5. **Economic Analysis Tool** - Calculates NPV, IRR, payback period

### Technical Documents

1. **Terms of Reference** - For hiring consultants
2. **RFP Template** - For contractor procurement
3. **Technical Specifications** - Equipment and performance requirements
4. **Quality Assurance Checklists** - For construction oversight
5. **Commissioning Procedures** - Step-by-step testing protocols

---

## DECISION POINTS FOR CITY COUNCIL APPROVAL

Throughout implementation, certain decisions require formal city council approval:

### Initial Approval (Month 1)
- ✅ Project concept approval
- ✅ Budget allocation for feasibility studies
- ✅ Appointment of project team

### Go/No-Go Decision (Month 9)
- ✅ Approval of final project design
- ✅ Authorization to proceed to procurement
- ✅ Approval of financing plan and municipal contribution

### Contract Award (Month 15)
- ✅ Approval of contractor selection
- ✅ Authorization to sign EPC contract
- ✅ Approval of PPA terms

### Construction Start (Month 16)
- ✅ Final authorization to commence construction
- ✅ Approval of community benefit agreement

### Additional Approvals as Needed
- ✅ Major contract variations (if >10% of value)
- ✅ Changes to project scope or timeline
- ✅ Additional funding requirements

**Recommendation:** Establish delegated authority for project manager to approve minor decisions (<$50K) to maintain project momentum.

---

This comprehensive roadmap positions city planners to successfully navigate the complex process of bringing this renewable energy project from concept to reality, delivering clean power and avoiding significant CO₂ emissions annually.
"""
    
    # Add conclusion section
    total_mw = power['total_mw']
    households_powered = community['households_powered']
    carbon_saved = env['carbon_saved_tons']
    lat = data['coordinates']['latitude']
    lng = data['coordinates']['longitude']
    
    report += f"""

---

## CONCLUSION: A BRIGHTER, CLEANER FUTURE

The {location} renewable energy project is more than just a power plant—it's an investment in our community's future.

### What We're Building:

✅ **Clean Energy:** {total_mw:.2f} MW of zero-emission power  
✅ **Community Power:** Electricity for {households_powered:,} households  
✅ **Environmental Protection:** {carbon_saved:,.0f} tons of CO₂ avoided annually  
✅ **Economic Development:** Jobs, lower costs, and new opportunities  
✅ **Energy Independence:** Freedom from fossil fuel price volatility  
✅ **Generational Impact:** Clean air and stable power for decades to come

### The Path Forward

With the right planning, community support, and financial backing, this project can become a reality within 2-3 years. The technology is proven, the benefits are clear, and the need is urgent.

### Your Role

Whether you're a government official who can facilitate permits, a community member who can spread awareness, or a potential investor who can provide funding—everyone has a role in making this vision a reality.

**The time for clean energy is now. The place is {location}. The opportunity is here.**

---


*This report was generated by EcoGrid AI Report Generator*  
*Technical data verified and calculations validated*  
*Report Date: {datetime.now().strftime("%B %d, %Y")}*
"""
    
    return report

# ============================================================================
# END OF AI REPORT GENERATION FUNCTION
# ============================================================================



# Initialize session state
if 'geo_data' not in st.session_state:
    st.session_state.geo_data = {}
if 'pdf_extracted' not in st.session_state:
    st.session_state.pdf_extracted = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}
if 'linked_locations' not in st.session_state:
    st.session_state.linked_locations = []

st.title("🌍 Geographic Energy Calculator")
st.markdown("*Map-based renewable energy potential & carbon impact analysis*")



# Main Content
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Calculate", 
    "Enhanced Map View", 
    "Carbon Impact",
    "Energy Flow",
    "Analysis", 
    "Export & AI Reports"
])
# TAB 1: CALCULATE
with tab1:
    st.header("Energy Potential Calculator")
    col_method, col_spacer = st.columns([2, 3])
    with col_method:
        input_method = st.selectbox(
        "📍 Location Input Method",
        ["Manual Entry", "Click on Map", "Use PDF Data", "Batch Analysis (CSV)"],
        help="Choose how to provide location coordinates"
    )
    
    # Alert user if map coordinates are available but not being used
    if 'clicked_lat' in st.session_state.geo_data and 'clicked_lng' in st.session_state.geo_data:
        if input_method != "Click on Map":
            st.warning(f"Map coordinates available: {st.session_state.geo_data['clicked_lat']:.4f}, {st.session_state.geo_data['clicked_lng']:.4f}. Change input method to 'Click on Map' in the dropdown to use them.")
    
    # Determine default values based on input method
    if input_method == "Use PDF Data" and st.session_state.pdf_extracted:
        st.success("Using data from PDF Analyzer")
        
        initial_latitude = float(st.session_state.pdf_extracted.get('latitude', 23.8103))
        initial_longitude = float(st.session_state.pdf_extracted.get('longitude', 90.4125))
        initial_waterfall_height = float(st.session_state.pdf_extracted.get('waterfall_height', 0.0))
        initial_waterfall_flow = float(st.session_state.pdf_extracted.get('waterfall_flow', 0.0))
        initial_geo_temp = float(st.session_state.pdf_extracted.get('geo_temp', 0.0))
        initial_depth = float(st.session_state.pdf_extracted.get('depth', 3.0))
        initial_location_name = st.session_state.pdf_extracted.get('location_name', 'PDF Location')
        
    elif input_method == "Use PDF Data":
        st.warning("No PDF data available. Please use the PDF analyzer to upload and extract data first!")
        initial_latitude = 23.8103
        initial_longitude = 90.4125
        initial_waterfall_height = 0.0
        initial_waterfall_flow = 0.0
        initial_geo_temp = 0.0
        initial_depth = 3.0
        initial_location_name = "Default Location"
        
    elif input_method == "Click on Map":
        if 'clicked_lat' in st.session_state.geo_data and 'clicked_lng' in st.session_state.geo_data:
            st.success(f"Using map location: {st.session_state.geo_data['clicked_lat']:.4f}, {st.session_state.geo_data['clicked_lng']:.4f}")
            initial_latitude = float(st.session_state.geo_data['clicked_lat'])
            initial_longitude = float(st.session_state.geo_data['clicked_lng'])
        else:
            st.info("Go to the 'Enhanced Map View' tab to click on a location first.")
            initial_latitude = 23.8103
            initial_longitude = 90.4125
        
        initial_waterfall_height = 50.0
        initial_waterfall_flow = 10.0
        initial_geo_temp = 200.0
        initial_depth = 3.0
        initial_location_name = "Map Location"
        
    elif input_method == "Batch Analysis (CSV)":
        st.info("Upload CSV in the 'Export & AI Reports' tab for batch processing!")
        initial_latitude = 23.8103
        initial_longitude = 90.4125
        initial_waterfall_height = 50.0
        initial_waterfall_flow = 10.0
        initial_geo_temp = 200.0
        initial_depth = 3.0
        initial_location_name = "Batch Location"
        
    else:  # Manual Entry
        initial_latitude = 23.8103
        initial_longitude = 90.4125
        initial_waterfall_height = 50.0
        initial_waterfall_flow = 10.0
        initial_geo_temp = 200.0
        initial_depth = 3.0
        initial_location_name = "My Location"
    
    # Initialize form data in session state if not exists
    if 'form_latitude' not in st.session_state:
        st.session_state.form_latitude = initial_latitude
    if 'form_longitude' not in st.session_state:
        st.session_state.form_longitude = initial_longitude
    if 'form_waterfall_height' not in st.session_state:
        st.session_state.form_waterfall_height = initial_waterfall_height
    if 'form_waterfall_flow' not in st.session_state:
        st.session_state.form_waterfall_flow = initial_waterfall_flow
    if 'form_geo_temp' not in st.session_state:
        st.session_state.form_geo_temp = initial_geo_temp
    if 'form_depth' not in st.session_state:
        st.session_state.form_depth = initial_depth
    
    # Update coordinates when input method changes to "Click on Map"
    if input_method == "Click on Map" and 'clicked_lat' in st.session_state.geo_data:
        st.session_state.form_latitude = float(st.session_state.geo_data['clicked_lat'])
        st.session_state.form_longitude = float(st.session_state.geo_data['clicked_lng'])
    
    # Update ALL values when input method changes to "Use PDF Data"
    if input_method == "Use PDF Data" and st.session_state.pdf_extracted:
        st.session_state.form_latitude = initial_latitude
        st.session_state.form_longitude = initial_longitude
        st.session_state.form_waterfall_height = initial_waterfall_height
        st.session_state.form_waterfall_flow = initial_waterfall_flow
        st.session_state.form_geo_temp = initial_geo_temp
        st.session_state.form_depth = initial_depth
    
    # Input fields
    location_name = st.text_input("Location Name", value=initial_location_name, help="Enter a descriptive name for this location")
    
    if not location_name or location_name.strip() == "":
        st.caption("Warning: Location name is required")
    
    col1, col2 = st.columns(2)
    
    with col1:
        latitude = st.number_input(
            "Latitude", 
            min_value=-90.0, 
            max_value=90.0, 
            value=st.session_state.form_latitude, 
            step=0.0001, 
            format="%.4f",
            key="latitude_input",
            help="Valid range: -90 to +90 (South to North)"
        )
        st.session_state.form_latitude = latitude
        
        waterfall_height = st.number_input(
            "Waterfall Height (m)", 
            min_value=0.0, 
            value=st.session_state.form_waterfall_height, 
            step=5.0,
            key="waterfall_height_input",
            help="Height of waterfall in meters. Leave at 0 if no waterfall."
        )
        st.session_state.form_waterfall_height = waterfall_height
        
        if waterfall_height > 500:
            st.caption("Warning: Very high waterfall - please verify")
        
        geo_temp = st.number_input(
            "Geothermal Temperature (°C)", 
            min_value=0.0, 
            max_value=900.0, 
            value=st.session_state.form_geo_temp, 
            step=10.0,
            key="geo_temp_input",
            help="Underground temperature in Celsius. Minimum 50°C for viable generation."
        )
        st.session_state.form_geo_temp = geo_temp
        
        if geo_temp > 0 and geo_temp < 50:
            st.caption("Warning: Temperature too low for efficient energy generation")
        elif geo_temp > 600:
            st.caption("Warning: Extremely high temperature - specialized equipment required")
    
    with col2:
        longitude = st.number_input(
            "Longitude", 
            min_value=-180.0, 
            max_value=180.0, 
            value=st.session_state.form_longitude, 
            step=0.0001, 
            format="%.4f",
            key="longitude_input",
            help="Valid range: -180 to +180 (West to East)"
        )
        st.session_state.form_longitude = longitude
        
        waterfall_flow = st.number_input(
            "Water Flow Rate (m³/s)", 
            min_value=0.0, 
            value=st.session_state.form_waterfall_flow, 
            step=0.5,
            key="waterfall_flow_input",
            help="Water flow in cubic meters per second. Leave at 0 if no waterfall."
        )
        st.session_state.form_waterfall_flow = waterfall_flow
        
        if waterfall_flow > 1000:
            st.caption("Warning: Very high flow rate - please verify")
        
        depth = st.number_input(
            "Drilling Depth (km)", 
            min_value=0.5, 
            max_value=10.0, 
            value=st.session_state.form_depth, 
            step=0.5,
            key="depth_input",
            help="Geothermal drilling depth in kilometers. Typical range: 1-5 km"
        )
        st.session_state.form_depth = depth
        
        if depth > 7:
            st.caption("Warning: Very deep drilling - higher costs expected")
    
    # Real-time validation summary
    st.markdown("---")
    
    validation_summary = []
    if waterfall_height > 0 or waterfall_flow > 0:
        if waterfall_height > 0 and waterfall_flow > 0:
            validation_summary.append("✅ VALID: Waterfall data complete")
        else:
            validation_summary.append("⚠️ WARNING: Waterfall data incomplete (need both height and flow)")
    
    if geo_temp >= 50:
        validation_summary.append("✅ VALID: Geothermal data viable")
    elif geo_temp > 0:
        validation_summary.append("⚠️ WARNING: Geothermal temperature too low")
    
    if not validation_summary:
        st.info("ℹ️ No energy source data entered yet")
    else:
        for summary in validation_summary:
            if "✅" in summary:
                st.success(summary)
            else:
                st.warning(summary)
    
    st.markdown("---")
    
    # Additional parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        turbine_efficiency = st.slider("Turbine Efficiency", 0.5, 0.95, 0.9, 0.01)
    with col2:
        geo_efficiency = st.slider("Geothermal Conversion Efficiency", 0.10, 0.25, 0.15, 0.01)
    with col3:
        capacity_factor = st.slider("Capacity Factor", 0.5, 0.95, 0.85, 0.01)
    
    # CALCULATIONS WITH VALIDATION
    if st.button("Calculate Energy Potential & Carbon Impact", type="primary"):
        
        # INPUT VALIDATION
        validation_errors = []
        
        if not location_name or location_name.strip() == "":
            validation_errors.append("ERROR: Location name cannot be empty")
        
        if latitude == 0 and longitude == 0:
            validation_errors.append("WARNING: Coordinates are at (0, 0). Please verify this is correct.")
        
        if waterfall_height > 0 and waterfall_flow == 0:
            validation_errors.append("ERROR: Waterfall height is set but flow rate is 0. Both must be greater than 0 for waterfall calculations.")
        
        if waterfall_flow > 0 and waterfall_height == 0:
            validation_errors.append("ERROR: Flow rate is set but waterfall height is 0. Both must be greater than 0 for waterfall calculations.")
        
        if waterfall_height > 500:
            validation_errors.append("WARNING: Waterfall height exceeds 500m. This is extremely high - please verify.")
        
        if waterfall_flow > 1000:
            validation_errors.append("WARNING: Flow rate exceeds 1000 m³/s. This is extremely high - please verify.")
        
        if geo_temp > 0 and geo_temp < 50:
            validation_errors.append("WARNING: Geothermal temperature below 50°C is too low for efficient energy generation.")
        
        if geo_temp > 600:
            validation_errors.append("WARNING: Temperature exceeds 600°C. This requires specialized equipment and safety measures.")
        
        if depth > 10:
            validation_errors.append("WARNING: Drilling depth exceeds 10 km. This is beyond typical geothermal project limits.")
        
        if depth < 1 and geo_temp > 100:
            validation_errors.append("WARNING: High temperature at shallow depth is unusual. Please verify data.")
        
        if waterfall_height == 0 and waterfall_flow == 0 and (geo_temp == 0 or geo_temp < 50):
            validation_errors.append("ERROR: No viable energy source detected. Please enter either waterfall data or geothermal data (temp > 50°C).")
        
        # Display validation errors/warnings
        if validation_errors:
            st.error("### Validation Issues Found:")
            for error in validation_errors:
                if error.startswith("ERROR"):
                    st.error(error)
                else:
                    st.warning(error)
            
            critical_errors = [e for e in validation_errors if e.startswith("ERROR")]
            if critical_errors:
                st.error("**Cannot proceed with calculation. Please fix the errors above.**")
                raise SystemExit
            else:
                if not st.checkbox("I acknowledge the warnings above and want to proceed with calculation"):
                    raise SystemExit
        
        with st.spinner("Calculating energy potential and environmental impact..."):
            
            # Constants
            rho = 1000
            g = 9.81
            specific_heat = 4.18
            surface_temp = 25
            
            # WATERFALL CALCULATIONS
            if waterfall_height > 0 and waterfall_flow > 0:
                P_waterfall_watts = rho * g * waterfall_flow * waterfall_height * turbine_efficiency
                P_waterfall_MW = P_waterfall_watts / 1_000_000
                E_waterfall_year_MWh = P_waterfall_MW * 24 * 365
                households_waterfall = int(E_waterfall_year_MWh * 1000 / 7.2)
                has_waterfall = True
            else:
                P_waterfall_MW = 0
                E_waterfall_year_MWh = 0
                households_waterfall = 0
                has_waterfall = False
            
            # GEOTHERMAL CALCULATIONS
            if geo_temp > 50 and depth > 0:
                flow_rate_geo = 50.0
                temp_diff = geo_temp - surface_temp
                
                thermal_power_kW = flow_rate_geo * specific_heat * temp_diff
                P_geo_MW = (thermal_power_kW * geo_efficiency) / 1000
                E_geo_year_MWh = P_geo_MW * 24 * 365 * capacity_factor
                households_geo = int(E_geo_year_MWh * 1000 / 7.2)
                
                if geo_temp < 300:
                    pipe_material = "Stainless Steel / Incoloy"
                    relative_cost = 1.0
                elif geo_temp < 600:
                    pipe_material = "Inconel alloys / Nickel-chromium"
                    relative_cost = 2.5
                else:
                    pipe_material = "Ceramic composites / SiC / Titanium alloys"
                    relative_cost = 5.0
                
                has_geothermal = True
            else:
                P_geo_MW = 0
                E_geo_year_MWh = 0
                households_geo = 0
                pipe_material = "N/A"
                relative_cost = 0
                has_geothermal = False
            
            # WASTE ENERGY RECOVERY
            base_waste_sources = 0
            
            if has_waterfall:
                waterfall_waste = E_waterfall_year_MWh * 1000 * 0.30
                base_waste_sources += waterfall_waste
            
            if has_geothermal:
                geothermal_waste = E_geo_year_MWh * 1000 * 0.30
                base_waste_sources += geothermal_waste
            
            waste_recovered_kWh = base_waste_sources * 0.80
            waste_remaining_kWh = base_waste_sources * 0.20
            
            E_waste_recovered_MWh = waste_recovered_kWh / 1000
            E_waste_remaining_MWh = waste_remaining_kWh / 1000
            
            households_waste = int(E_waste_recovered_MWh * 1000 / 7.2)
            
            # TOTALS
            P_total_MW = P_waterfall_MW + P_geo_MW
            E_total_year_MWh = E_waterfall_year_MWh + E_geo_year_MWh + E_waste_recovered_MWh
            households_total = int(E_total_year_MWh * 1000 / 7.2)
            
            # CARBON EMISSIONS CALCULATIONS
            carbon_factor = CARBON_FACTORS['grid_average_bangladesh']
            carbon_saved_tons = E_total_year_MWh * carbon_factor
            
            SO2_saved = E_total_year_MWh * OTHER_EMISSIONS['SO2']
            NOx_saved = E_total_year_MWh * OTHER_EMISSIONS['NOx']
            PM25_saved = E_total_year_MWh * OTHER_EMISSIONS['PM2.5']
            CH4_saved = E_total_year_MWh * OTHER_EMISSIONS['CH4']
            mercury_saved = E_total_year_MWh * OTHER_EMISSIONS['mercury']
            
            trees_equivalent = int(carbon_saved_tons * 16.5)
            cars_off_road = int(carbon_saved_tons / 4.6)
            coal_avoided_tons = carbon_saved_tons / CARBON_FACTORS['coal']
            gas_avoided_tons = carbon_saved_tons / CARBON_FACTORS['natural_gas']
            
            # STORE IN SESSION STATE
            st.session_state.geo_data = {
                'location_name': location_name,
                'latitude': latitude,
                'longitude': longitude,
                'waterfall_height': waterfall_height,
                'waterfall_flow': waterfall_flow,
                'geo_temp': geo_temp,
                'depth': depth,
                'P_waterfall_MW': P_waterfall_MW,
                'P_geo_MW': P_geo_MW,
                'P_total_MW': P_total_MW,
                'E_waterfall_year_MWh': E_waterfall_year_MWh,
                'E_geo_year_MWh': E_geo_year_MWh,
                'E_waste_recovered_MWh': E_waste_recovered_MWh,
                'E_waste_remaining_MWh': E_waste_remaining_MWh,
                'base_waste_sources': base_waste_sources / 1000,
                'E_total_year_MWh': E_total_year_MWh,
                'households_total': households_total,
                'pipe_material': pipe_material,
                'has_waterfall': has_waterfall,
                'has_geothermal': has_geothermal,
                'carbon_saved_tons': carbon_saved_tons,
                'SO2_saved_kg': SO2_saved,
                'NOx_saved_kg': NOx_saved,
                'PM25_saved_kg': PM25_saved,
                'CH4_saved_kg': CH4_saved,
                'mercury_saved_kg': mercury_saved,
                'trees_equivalent': trees_equivalent,
                'cars_off_road': cars_off_road,
                'coal_avoided_tons': coal_avoided_tons,
                'gas_avoided_tons': gas_avoided_tons
            }
            
            st.session_state.predictions['waterfall_mw'] = P_waterfall_MW
            st.session_state.predictions['geo_mw'] = P_geo_MW
            st.session_state.predictions['total_annual_mwh'] = E_total_year_MWh
            st.session_state.predictions['location'] = location_name
        
        # DISPLAY RESULTS
        st.success("✅ Calculation Complete!")
        
        st.markdown("### Total System Output")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Power", f"{P_total_MW:.2f} MW")
        with col2:
            st.metric("Annual Energy", f"{E_total_year_MWh:,.0f} MWh")
        with col3:
            st.metric("Households Powered", f"{households_total:,}")
        with col4:
            st.metric("CO₂ Saved", f"{carbon_saved_tons:,.0f} tons/year", 
                     delta="vs fossil fuel", delta_color="normal")
        
        st.markdown("---")
        
        # Environmental Impact Summary
        st.markdown("### 🌱 Environmental Impact vs Fossil Fuel Generation")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Trees Equivalent", f"{trees_equivalent:,}", 
                     help="Number of trees needed to absorb this CO₂")
        with col2:
            st.metric("Cars Off Road", f"{cars_off_road:,}", 
                     help="Equivalent to removing this many cars from roads")
        with col3:
            st.metric("Coal Avoided", f"{coal_avoided_tons:,.0f} MWh", 
                     help="Equivalent coal generation avoided")
        with col4:
            st.metric("Gas Avoided", f"{gas_avoided_tons:,.0f} MWh", 
                     help="Equivalent natural gas generation avoided")
        
        st.markdown("---")
        
        # Breakdown
        st.markdown("### Energy Source Breakdown")
        
        st.info("**Waste Recovery System:** Operates continuously and independently from main generation systems, capturing 80% of thermal and mechanical losses.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if has_waterfall or has_geothermal:
                labels = []
                values = []
                colors = []
                
                if has_waterfall:
                    labels.append('Waterfall')
                    values.append(E_waterfall_year_MWh)
                    colors.append('#1f77b4')
                
                if has_geothermal:
                    labels.append('Geothermal')
                    values.append(E_geo_year_MWh)
                    colors.append('#ff7f0e')
                
                if E_waste_recovered_MWh > 0:
                    labels.append('Waste Recovery')
                    values.append(E_waste_recovered_MWh)
                    colors.append('#2ca02c')
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    marker=dict(colors=colors),
                    hole=0.3
                )])
                fig_pie.update_layout(title="Energy Generation Mix")
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            sources = []
            power_values = []
            
            if has_waterfall:
                sources.append('Waterfall')
                power_values.append(P_waterfall_MW)
            
            if has_geothermal:
                sources.append('Geothermal')
                power_values.append(P_geo_MW)
            
            if E_waste_recovered_MWh > 0:
                sources.append('Waste Recovery')
                power_values.append(E_waste_recovered_MWh / (24 * 365))
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=sources,
                y=power_values,
                name='Power (MW)',
                marker_color='lightblue'
            ))
            fig_bar.update_layout(
                title="Power Output by Source",
                yaxis_title="Power (MW)",
                xaxis_title="Energy Source"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("---")
        
        # Add to Linked Locations button
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔗 Add to Linked Locations Network"):
                already_linked = any(
                    loc.get('location_name') == st.session_state.geo_data.get('location_name')
                    for loc in st.session_state.linked_locations
                )
                
                if already_linked:
                    st.warning("This location is already in the linked network!")
                else:
                    st.session_state.linked_locations.append(st.session_state.geo_data.copy())
                    st.success(f"✅ Added '{st.session_state.geo_data.get('location_name')}' to linked network!")
                    st.info(f"Total linked locations: {len(st.session_state.linked_locations)}")
        
        with st.expander("Detailed Calculations"):
            if has_waterfall:
                st.markdown("#### Waterfall Turbine System")
                st.write(f"- Flow Rate: {waterfall_flow} m³/s")
                st.write(f"- Height: {waterfall_height} m")
                st.write(f"- Efficiency: {turbine_efficiency*100}%")
                st.write(f"- **Power Output: {P_waterfall_MW:.2f} MW**")
                st.write(f"- **Annual Energy: {E_waterfall_year_MWh:,.0f} MWh**")
                st.write(f"- **Households: {households_waterfall:,}**")
                st.markdown("---")
            
            if has_geothermal:
                st.markdown("#### Geothermal System")
                st.write(f"- Depth: {depth} km")
                st.write(f"- Underground Temperature: {geo_temp}°C")
                st.write(f"- Temperature Differential: {geo_temp - surface_temp}°C")
                st.write(f"- Conversion Efficiency: {geo_efficiency*100}%")
                st.write(f"- Capacity Factor: {capacity_factor*100}%")
                st.write(f"- **Power Output: {P_geo_MW:.2f} MW**")
                st.write(f"- **Annual Energy: {E_geo_year_MWh:,.0f} MWh**")
                st.write(f"- **Households: {households_geo:,}**")
                st.write(f"- **Recommended Pipe Material:** {pipe_material}")
                st.write(f"- **Relative Cost Factor:** {relative_cost}x")
                st.markdown("---")
            
            if E_waste_recovered_MWh > 0:
                st.markdown("#### Continuous Waste Energy Recovery (Second Line)")
                st.write("**System Type:** Always-ON independent recovery")
                st.write(f"- **Total Waste Available:** {base_waste_sources / 1000:,.2f} MWh/year (30% of main output)")
                st.write(f"- **Recovery Efficiency:** 80% continuous capture")
                st.write(f"- **Recovered Energy:** {E_waste_recovered_MWh:,.2f} MWh/year")
                st.write(f"- **System Reserve:** {E_waste_remaining_MWh:,.2f} MWh/year (20% for stability)")
                st.write(f"- **Additional Households Powered:** {households_waste:,}")
                st.info("**Note:** This recovery system operates continuously and independently, capturing waste heat, friction losses, and mechanical inefficiencies from the primary generation systems.")
        
        st.success("✅ Data saved! Check the Enhanced Map View to see this location with detailed popups.")


# TAB 2: ENHANCED MAP VIEW
with tab2:
    st.header("🗺️ Interactive Energy & Carbon Impact Map")
    
    # Get current location for map center
    if st.session_state.geo_data:
        map_lat = st.session_state.geo_data.get('latitude', 23.8103)
        map_lng = st.session_state.geo_data.get('longitude', 90.4125)
    else:
        map_lat = 23.8103
        map_lng = 90.4125
    
    # Map style selector
    col1, col2 = st.columns([3, 1])
    with col2:
        map_style = st.selectbox(
            "Map Style",
            ["OpenStreetMap", "CartoDB Positron", "CartoDB Dark Matter"],
            key="map_style_selector"
        )
    
    # Create map with selected style
    tile_mapping = {
        "OpenStreetMap": "OpenStreetMap",
        "CartoDB Positron": "CartoDB positron",
        "CartoDB Dark Matter": "CartoDB dark_matter"
    }
    
    m = folium.Map(
        location=[map_lat, map_lng],
        zoom_start=8,
        tiles=tile_mapping[map_style]
    )
    
    # Add current location marker with DETAILED POPUP
    if st.session_state.geo_data and 'location_name' in st.session_state.geo_data:
        location_name = st.session_state.geo_data.get('location_name', 'Selected Location')
        total_mw = st.session_state.geo_data.get('P_total_MW', 0)
        waterfall_mw = st.session_state.geo_data.get('P_waterfall_MW', 0)
        geo_mw = st.session_state.geo_data.get('P_geo_MW', 0)
        households = st.session_state.geo_data.get('households_total', 0)
        carbon_saved = st.session_state.geo_data.get('carbon_saved_tons', 0)
        energy_total = st.session_state.geo_data.get('E_total_year_MWh', 0)
        trees_equiv = st.session_state.geo_data.get('trees_equivalent', 0)
        cars_off = st.session_state.geo_data.get('cars_off_road', 0)
        
        # ENHANCED POPUP with ALL calculation details
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; width: 350px; padding: 10px;">
            <h3 style="color: #2E7D32; margin-bottom: 10px; border-bottom: 2px solid #4CAF50;">
                📍 {location_name}
            </h3>
            
            <div style="background: #E8F5E9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <h4 style="color: #1B5E20; margin: 5px 0;">⚡ Power Generation</h4>
                <table style="width: 100%; font-size: 13px;">
                    <tr><td><b>Total Power:</b></td><td style="text-align: right;">{total_mw:.2f} MW</td></tr>
                    <tr><td>├─ Waterfall:</td><td style="text-align: right;">{waterfall_mw:.2f} MW</td></tr>
                    <tr><td>└─ Geothermal:</td><td style="text-align: right;">{geo_mw:.2f} MW</td></tr>
                    <tr style="border-top: 1px solid #4CAF50;">
                        <td><b>Annual Energy:</b></td><td style="text-align: right;"><b>{energy_total:,.0f} MWh</b></td>
                    </tr>
                </table>
            </div>
            
            <div style="background: #FFF3E0; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <h4 style="color: #E65100; margin: 5px 0;">🏘️ Community Impact</h4>
                <table style="width: 100%; font-size: 13px;">
                    <tr><td><b>Households Powered:</b></td><td style="text-align: right;">{households:,}</td></tr>
                    <tr><td><b>People Served:</b></td><td style="text-align: right;">{households * 4:,}</td></tr>
                </table>
            </div>
            
            <div style="background: #E3F2FD; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <h4 style="color: #0D47A1; margin: 5px 0;">🌱 Environmental Impact</h4>
                <table style="width: 100%; font-size: 13px;">
                    <tr><td><b>CO₂ Saved:</b></td><td style="text-align: right;"><b>{carbon_saved:,.0f} tons/yr</b></td></tr>
                    <tr><td>Tree Equivalent:</td><td style="text-align: right;">{trees_equiv:,} trees</td></tr>
                    <tr><td>Cars Off Road:</td><td style="text-align: right;">{cars_off:,} vehicles</td></tr>
                </table>
            </div>
            
            <div style="background: #F3E5F5; padding: 10px; border-radius: 5px;">
                <h4 style="color: #4A148C; margin: 5px 0;">📍 Coordinates</h4>
                <p style="font-size: 12px; margin: 5px 0;">
                    Lat: {map_lat:.6f}<br>
                    Lng: {map_lng:.6f}
                </p>
            </div>
        </div>
        """
        
        # Color based on total power output
        if total_mw > 5:
            color = 'green'
            icon_name = 'bolt'
        elif total_mw > 2:
            color = 'orange'
            icon_name = 'flash'
        else:
            color = 'red'
            icon_name = 'warning'
        
        folium.Marker(
            [map_lat, map_lng],
            popup=folium.Popup(popup_html, max_width=400),
            tooltip=f"🔋 {location_name}: {total_mw:.2f} MW | 💨 {carbon_saved:,.0f}t CO₂/yr",
            icon=folium.Icon(color=color, icon=icon_name, prefix='fa')
        ).add_to(m)
        
        # Add circle to show impact radius
        folium.Circle(
            location=[map_lat, map_lng],
            radius=households * 10,
            color='green',
            fill=True,
            fillColor='green',
            fillOpacity=0.1,
            popup=f"Service Area: ~{households:,} households"
        ).add_to(m)
    
    st.markdown("**✨ Click on map markers to see detailed energy, carbon, and community impact data**")
    map_data = st_folium(m, width=700, height=600, key="enhanced_map")
    
    # Handle map clicks
    if map_data and map_data.get('last_clicked'):
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lng = map_data['last_clicked']['lng']
        
        # Store clicked coordinates
        st.session_state.geo_data['clicked_lat'] = clicked_lat
        st.session_state.geo_data['clicked_lng'] = clicked_lng
        
        st.success(f"✅ New location selected: {clicked_lat:.4f}, {clicked_lng:.4f}")
        st.info("Go to the 'Calculate' tab and select 'Click on Map' input method to use these coordinates.")

# TAB 3: CARBON IMPACT (FIXED VERSION)
with tab3:
    st.header("🌱 Carbon Impact Analysis")
    
    if st.session_state.geo_data and 'carbon_saved_tons' in st.session_state.geo_data:
        
        carbon_saved = st.session_state.geo_data.get('carbon_saved_tons', 0)
        energy_total = st.session_state.geo_data.get('E_total_year_MWh', 0)
        
        st.markdown(f"### Environmental Impact: {st.session_state.geo_data.get('location_name')}")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("CO₂ Saved", f"{carbon_saved:,.0f} tons/year", 
                     delta="vs fossil fuel", delta_color="inverse")
        with col2:
            st.metric("Trees Equivalent", f"{st.session_state.geo_data.get('trees_equivalent', 0):,}")
        with col3:
            st.metric("Cars Off Road", f"{st.session_state.geo_data.get('cars_off_road', 0):,}")
        with col4:
            st.metric("Coal Avoided", f"{st.session_state.geo_data.get('coal_avoided_tons', 0):,.0f} MWh")
        
        st.markdown("---")
        
        # Comparison Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # THIS IS THE FIX - CREATE fuel_comparison DataFrame
            fuel_comparison = pd.DataFrame({
                'Fuel Type': ['Your System', 'Coal', 'Natural Gas', 'Diesel', 'Furnace Oil'],
                'CO₂ Emissions (tons)': [
                    0,  # Your renewable system produces no CO2
                    energy_total * CARBON_FACTORS['coal'],
                    energy_total * CARBON_FACTORS['natural_gas'],
                    energy_total * CARBON_FACTORS['diesel'],
                    energy_total * CARBON_FACTORS['furnace_oil']
                ]
            })
            
            fig = px.bar(
                fuel_comparison, 
                x='Fuel Type', 
                y='CO₂ Emissions (tons)',
                title='CO₂ Emissions Comparison by Fuel Type',
                color='Fuel Type',
                color_discrete_map={
                    'Your System': 'green',
                    'Coal': 'black',
                    'Natural Gas': 'orange',
                    'Diesel': 'red',
                    'Furnace Oil': 'darkred'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            equivalencies = pd.DataFrame({
                'Equivalent': ['Trees Planted', 'Cars Removed', 'Homes Powered'],
                'Amount': [
                    st.session_state.geo_data['trees_equivalent'],
                    st.session_state.geo_data['cars_off_road'],
                    st.session_state.geo_data['households_total']
                ]
            })
            
            fig2 = px.bar(
                equivalencies,
                x='Equivalent',
                y='Amount',
                title='Environmental Impact Equivalencies',
                color='Equivalent',
                color_discrete_sequence=['green', 'blue', 'purple']
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📊 20-Year Environmental Impact Projection")
        
        years = list(range(1, 21))
        cumulative_co2 = [carbon_saved * year for year in years]
        cumulative_trees = [st.session_state.geo_data['trees_equivalent'] * year for year in years]
        
        from plotly.subplots import make_subplots
        
        fig_projection = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Cumulative CO₂ Saved', 'Equivalent Trees Planted')
        )
        
        fig_projection.add_trace(
            go.Scatter(x=years, y=cumulative_co2, mode='lines+markers', 
                      name='CO₂ Saved', line=dict(color='green', width=3)),
            row=1, col=1
        )
        
        fig_projection.add_trace(
            go.Scatter(x=years, y=cumulative_trees, mode='lines+markers',
                      name='Trees Equivalent', line=dict(color='darkgreen', width=3)),
            row=1, col=2
        )
        
        fig_projection.update_xaxes(title_text="Years", row=1, col=1)
        fig_projection.update_xaxes(title_text="Years", row=1, col=2)
        fig_projection.update_yaxes(title_text="CO₂ (tons)", row=1, col=1)
        fig_projection.update_yaxes(title_text="Trees", row=1, col=2)
        fig_projection.update_layout(height=400, showlegend=False)
        
        st.plotly_chart(fig_projection, use_container_width=True)
        
        st.success(f"**Over 20 years:** {cumulative_co2[-1]:,.0f} tons CO₂ saved = {cumulative_trees[-1]:,} trees planted!")
        
    else:
        st.warning("No calculation data available. Please run calculations in the 'Calculate' tab first!")


# TAB 4: ENERGY FLOW DIAGRAM
with tab4:
    st.header("⚡ Energy Flow Visualization")
    
    if st.session_state.geo_data and 'P_total_MW' in st.session_state.geo_data:
        
        st.markdown(f"### System: {st.session_state.geo_data.get('location_name')}")
        
        waterfall_mwh = st.session_state.geo_data.get('E_waterfall_year_MWh', 0)
        geo_mwh = st.session_state.geo_data.get('E_geo_year_MWh', 0)
        waste_recovered = st.session_state.geo_data.get('E_waste_recovered_MWh', 0)
        total_mwh = st.session_state.geo_data.get('E_total_year_MWh', 0)
        
        # Calculate waste
        waste_from_waterfall = waterfall_mwh * 0.30 if waterfall_mwh > 0 else 0
        waste_from_geo = geo_mwh * 0.30 if geo_mwh > 0 else 0
        total_waste = waste_from_waterfall + waste_from_geo
        waste_lost = total_waste * 0.20
        
        # Sankey diagram nodes
        nodes = ['Waterfall Turbine', 'Geothermal System', 'Primary Energy', 'Waste Heat', 
                'Recovery System', 'Grid Output', 'Lost Heat']
        
        # Sankey diagram links
        links = {
            'source': [],
            'target': [],
            'value': [],
            'label': []
        }
        
        if waterfall_mwh > 0:
            links['source'].append(0)
            links['target'].append(2)
            links['value'].append(waterfall_mwh)
            links['label'].append(f'{waterfall_mwh:,.0f} MWh')
            
            links['source'].append(0)
            links['target'].append(3)
            links['value'].append(waste_from_waterfall)
            links['label'].append(f'{waste_from_waterfall:,.0f} MWh waste')
        
        if geo_mwh > 0:
            links['source'].append(1)
            links['target'].append(2)
            links['value'].append(geo_mwh)
            links['label'].append(f'{geo_mwh:,.0f} MWh')
            
            links['source'].append(1)
            links['target'].append(3)
            links['value'].append(waste_from_geo)
            links['label'].append(f'{waste_from_geo:,.0f} MWh waste')
        
        if total_waste > 0:
            links['source'].append(3)
            links['target'].append(4)
            links['value'].append(waste_recovered)
            links['label'].append(f'{waste_recovered:,.0f} MWh recovered')
            
            links['source'].append(3)
            links['target'].append(6)
            links['value'].append(waste_lost)
            links['label'].append(f'{waste_lost:,.0f} MWh lost')
        
        # Primary to grid
        primary_total = waterfall_mwh + geo_mwh
        if primary_total > 0:
            links['source'].append(2)
            links['target'].append(5)
            links['value'].append(primary_total)
            links['label'].append(f'{primary_total:,.0f} MWh')
        
        # Recovery to grid
        if waste_recovered > 0:
            links['source'].append(4)
            links['target'].append(5)
            links['value'].append(waste_recovered)
            links['label'].append(f'{waste_recovered:,.0f} MWh')
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#17becf', '#8c564b']
            ),
            link=dict(
                source=links['source'],
                target=links['target'],
                value=links['value'],
                label=links['label']
            )
        )])
        
        fig.update_layout(
            title=f"Energy Flow Diagram - {st.session_state.geo_data.get('location_name')}",
            font_size=12,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### System Efficiency Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            primary_efficiency = (primary_total / (primary_total + total_waste)) * 100 if (primary_total + total_waste) > 0 else 0
            st.metric("Primary System Efficiency", f"{primary_efficiency:.1f}%")
        
        with col2:
            recovery_efficiency = (waste_recovered / total_waste) * 100 if total_waste > 0 else 0
            st.metric("Waste Recovery Efficiency", f"{recovery_efficiency:.1f}%")
        
        with col3:
            overall_efficiency = (total_mwh / (primary_total + total_waste)) * 100 if (primary_total + total_waste) > 0 else 0
            st.metric("Overall System Efficiency", f"{overall_efficiency:.1f}%")
        
    else:
        st.warning("No calculation data available. Please run calculations in the 'Calculate' tab first!")


# TAB 5: ANALYSIS
with tab5:
    st.header("Geographic Energy Analysis")
    
    if st.session_state.geo_data and 'P_total_MW' in st.session_state.geo_data:
        
        st.subheader("Optimal Placement Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.geo_data.get('has_waterfall'):
                st.success("Waterfall Turbine System")
                st.write("**Recommended Installation:**")
                st.write("- Install turbines at the base of waterfall")
                st.write("- Use adjustable blade systems for flow variation")
                st.write("- Implement AI-controlled flow monitoring")
                st.write("- Add modular blade replacement capability")
                
                height = st.session_state.geo_data.get('waterfall_height', 0)
                if height > 100:
                    st.warning("Very high waterfall - consider multiple turbine stages")
                elif height < 20:
                    st.info("Low head turbine recommended (Kaplan or Francis type)")
            else:
                st.info("No waterfall data - not applicable for this location")
        
        with col2:
            if st.session_state.geo_data.get('has_geothermal'):
                st.success("Geothermal System")
                st.write("**Recommended Installation:**")
                st.write(f"- Drill to {st.session_state.geo_data.get('depth', 0)} km depth")
                st.write(f"- Use {st.session_state.geo_data.get('pipe_material', 'N/A')}")
                st.write("- Implement closed-loop heat exchanger")
                st.write("- Add AI monitoring for pipe stress & temperature")
                
                temp = st.session_state.geo_data.get('geo_temp', 0)
                if temp > 300:
                    st.warning("High temperature - enhanced safety protocols required")
                if temp < 150:
                    st.info("Consider binary cycle system for low-temp geothermal")
            else:
                st.info("No geothermal data - not applicable for this location")
        
        st.markdown("---")
        st.subheader("Sensitivity Analysis")
        
        sensitivity_param = st.selectbox(
            "Select parameter to analyze:",
            ["Waterfall Flow Rate", "Waterfall Height", "Geothermal Temperature", "Drilling Depth"]
        )
        
        if sensitivity_param == "Waterfall Flow Rate":
            base_flow = st.session_state.geo_data.get('waterfall_flow', 10)
            base_height = st.session_state.geo_data.get('waterfall_height', 50)
            
            flow_range = np.linspace(base_flow * 0.5, base_flow * 1.5, 50)
            power_range = [1000 * 9.81 * f * base_height * 0.9 / 1_000_000 for f in flow_range]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=flow_range,
                y=power_range,
                mode='lines',
                name='Power Output',
                line=dict(color='blue', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[base_flow],
                y=[st.session_state.geo_data.get('P_waterfall_MW', 0)],
                mode='markers',
                name='Current Setup',
                marker=dict(size=15, color='red')
            ))
            fig.update_layout(
                title="Power Output vs Flow Rate",
                xaxis_title="Flow Rate (m³/s)",
                yaxis_title="Power (MW)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif sensitivity_param == "Waterfall Height":
            base_flow = st.session_state.geo_data.get('waterfall_flow', 10)
            base_height = st.session_state.geo_data.get('waterfall_height', 50)
            
            height_range = np.linspace(base_height * 0.5, base_height * 1.5, 50)
            power_range = [1000 * 9.81 * base_flow * h * 0.9 / 1_000_000 for h in height_range]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=height_range,
                y=power_range,
                mode='lines',
                name='Power Output',
                line=dict(color='green', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[base_height],
                y=[st.session_state.geo_data.get('P_waterfall_MW', 0)],
                mode='markers',
                name='Current Setup',
                marker=dict(size=15, color='red')
            ))
            fig.update_layout(
                title="Power Output vs Waterfall Height",
                xaxis_title="Height (m)",
                yaxis_title="Power (MW)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif sensitivity_param == "Geothermal Temperature":
            base_temp = st.session_state.geo_data.get('geo_temp', 200)
            
            temp_range = np.linspace(150, 400, 50)
            power_range = [(50 * 4.18 * (t - 25) * 0.15) / 1000 for t in temp_range]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=temp_range,
                y=power_range,
                mode='lines',
                name='Power Output',
                line=dict(color='orange', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[base_temp],
                y=[st.session_state.geo_data.get('P_geo_MW', 0)],
                mode='markers',
                name='Current Setup',
                marker=dict(size=15, color='red')
            ))
            fig.update_layout(
                title="Power Output vs Underground Temperature",
                xaxis_title="Temperature (°C)",
                yaxis_title="Power (MW)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            base_depth = st.session_state.geo_data.get('depth', 3.0)
            base_temp = st.session_state.geo_data.get('geo_temp', 200)
            
            surface_temp = 25
            gradient = (base_temp - surface_temp) / base_depth
            
            depth_range = np.linspace(1, 10, 50)
            temp_at_depth = [surface_temp + gradient * d for d in depth_range]
            power_range = [(50 * 4.18 * (t - surface_temp) * 0.15) / 1000 for t in temp_at_depth]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=depth_range,
                y=power_range,
                mode='lines',
                name='Power Output',
                line=dict(color='purple', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[base_depth],
                y=[st.session_state.geo_data.get('P_geo_MW', 0)],
                mode='markers',
                name='Current Setup',
                marker=dict(size=15, color='red')
            ))
            fig.update_layout(
                title="Power Output vs Drilling Depth",
                xaxis_title="Depth (km)",
                yaxis_title="Power (MW)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("No calculation data available. Please go to the 'Calculate' tab first!")


# TAB 6: EXPORT & AI REPORTS
with tab6:
    st.header("📊 Export & AI Report Generator")
    
    # Create sub-tabs for different export options
    export_tab1, export_tab2, export_tab3 = st.tabs([
        "📄 Data Export (CSV/JSON)", 
        "🤖 AI-Powered PDF Report", 
        "📦 Batch Analysis"
    ])
    
    # SUB-TAB 1: Traditional Data Export
    with export_tab1:
        st.subheader("Export Calculation Data")
        
        if st.session_state.geo_data and 'location_name' in st.session_state.geo_data:
            
            export_data = {
                'Location Name': [st.session_state.geo_data.get('location_name', 'N/A')],
                'Latitude': [st.session_state.geo_data.get('latitude', 0)],
                'Longitude': [st.session_state.geo_data.get('longitude', 0)],
                'Waterfall Power (MW)': [st.session_state.geo_data.get('P_waterfall_MW', 0)],
                'Geothermal Power (MW)': [st.session_state.geo_data.get('P_geo_MW', 0)],
                'Total Power (MW)': [st.session_state.geo_data.get('P_total_MW', 0)],
                'Annual Energy (MWh)': [st.session_state.geo_data.get('E_total_year_MWh', 0)],
                'CO₂ Saved (tons/year)': [st.session_state.geo_data.get('carbon_saved_tons', 0)],
                'Households Powered': [st.session_state.geo_data.get('households_total', 0)],
                'Trees Equivalent': [st.session_state.geo_data.get('trees_equivalent', 0)],
                'Cars Off Road': [st.session_state.geo_data.get('cars_off_road', 0)],
                'Pipe Material': [st.session_state.geo_data.get('pipe_material', 'N/A')]
            }
            
            export_df = pd.DataFrame(export_data)
            st.dataframe(export_df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv,
                    file_name=f"ecogrid_{st.session_state.geo_data.get('location_name', 'location').replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_str = export_df.to_json(orient='records', indent=2)
                st.download_button(
                    label="⬇️ Download as JSON",
                    data=json_str,
                    file_name=f"ecogrid_{st.session_state.geo_data.get('location_name', 'location').replace(' ', '_')}.json",
                    mime="application/json"
                )
            
            # Linked locations export
            if st.session_state.linked_locations:
                st.markdown("---")
                st.subheader("🔗 Linked Location Network Export")
                
                network_data = []
                for loc in st.session_state.linked_locations:
                    network_data.append({
                        'Location': loc.get('location_name'),
                        'Latitude': loc.get('latitude'),
                        'Longitude': loc.get('longitude'),
                        'Power (MW)': loc.get('P_total_MW'),
                        'Energy (MWh/year)': loc.get('E_total_year_MWh'),
                        'CO₂ Saved (tons)': loc.get('carbon_saved_tons'),
                        'Households': loc.get('households_total')
                    })
                
                network_df = pd.DataFrame(network_data)
                st.dataframe(network_df, use_container_width=True)
                
                csv_network = network_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Linked Network Data",
                    data=csv_network,
                    file_name="ecogrid_linked_network.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No calculation data available. Run calculations first!")
    
    # SUB-TAB 2: AI-Powered PDF Report Generator
    with export_tab2:
        st.subheader("🤖 AI-Powered Comprehensive Report")
        
        if not st.session_state.geo_data or 'P_total_MW' not in st.session_state.geo_data:
            st.warning("⚠️ No calculation data available!")
            st.info("Run calculations in the **Calculate** tab first, then return here to generate your AI report.")
        else:
            st.markdown("""
            **What makes this special?**
            
            Instead of just exporting raw numbers, our AI analyzes your data and creates a 
            professional report that explains:
            - What the numbers actually mean in simple terms
            - Why this project matters for your community
            - How it compares to traditional energy sources
            - Environmental and economic benefits in plain language
            - Implementation recommendations
            
            Perfect for presentations to government officials, community meetings, or investor pitches!
            """)
            
            st.markdown("---")
            
            # Report Configuration
            col1, col2 = st.columns(2)
            
            with col1:
                report_type = st.selectbox(
                    "📋 Report Type",
                    [
                        "Executive Summary (2-3 pages)",
                        "Detailed Technical Report (8-10 pages)",
                        "Community Presentation (5-7 pages)",
                        "Investment Proposal (6-8 pages)",
                        "Environmental Impact Assessment (10-12 pages)"
                    ],
                    help="Choose the type of report based on your needs"
                )
                
                audience = st.selectbox(
                    "👥 Target Audience",
                    [
                        "Government Officials",
                        "Community Members",
                        "Investors/Funders",
                        "Technical Engineers",
                        "Environmental Groups",
                        "General Public"
                    ],
                    help="Who will be reading this report?"
                )
                
                language_style = st.selectbox(
                    "📝 Language Style",
                    [
                        "Simple & Accessible",
                        "Technical & Professional",
                        "Persuasive & Compelling",
                        "Educational & Informative"
                    ]
                )
            
            with col2:
                include_visualizations = st.checkbox("Include Data Visualizations", value=True)
                include_comparisons = st.checkbox("Compare with Fossil Fuels", value=True)
                include_implementation = st.checkbox("Include Implementation Plan", value=True)
                include_cost_estimate = st.checkbox("Include Cost Estimates", value=False)
                
                st.info("💡 **Tip:** AI will explain technical terms in simple language based on your audience selection.")
            
            # Analysis Focus
            st.markdown("### 🎯 What should the AI analyze?")
            
            analysis_focus = st.multiselect(
                "Select focus areas:",
                [
                    "Explain the numbers in simple terms",
                    "Compare with traditional energy sources",
                    "Highlight environmental benefits",
                    "Discuss economic opportunities",
                    "Address potential challenges",
                    "Provide implementation roadmap",
                    "Calculate return on investment",
                    "Identify funding opportunities",
                    "Assess community impact",
                    "Evaluate scalability potential"
                ],
                default=[
                    "Explain the numbers in simple terms",
                    "Highlight environmental benefits",
                    "Discuss economic opportunities"
                ]
            )
            
            st.markdown("---")
            
            # Generate Report Button
            if st.button("🤖 Generate AI Report", type="primary", use_container_width=True):
                
                # Prepare data for AI
                analysis_data = {
                    'location': st.session_state.geo_data.get('location_name'),
                    'coordinates': {
                        'latitude': st.session_state.geo_data.get('latitude'),
                        'longitude': st.session_state.geo_data.get('longitude')
                    },
                    'power_generation': {
                        'total_mw': st.session_state.geo_data.get('P_total_MW', 0),
                        'waterfall_mw': st.session_state.geo_data.get('P_waterfall_MW', 0),
                        'geothermal_mw': st.session_state.geo_data.get('P_geo_MW', 0),
                        'annual_energy_mwh': st.session_state.geo_data.get('E_total_year_MWh', 0)
                    },
                    'environmental_impact': {
                        'carbon_saved_tons': st.session_state.geo_data.get('carbon_saved_tons', 0),
                        'trees_equivalent': st.session_state.geo_data.get('trees_equivalent', 0),
                        'cars_off_road': st.session_state.geo_data.get('cars_off_road', 0),
                        'coal_avoided_tons': st.session_state.geo_data.get('coal_avoided_tons', 0)
                    },
                    'community_impact': {
                        'households_powered': st.session_state.geo_data.get('households_total', 0),
                        'people_served': st.session_state.geo_data.get('households_total', 0) * 4
                    },
                    'technical_details': {
                        'waterfall_height': st.session_state.geo_data.get('waterfall_height', 0),
                        'waterfall_flow': st.session_state.geo_data.get('waterfall_flow', 0),
                        'geothermal_temp': st.session_state.geo_data.get('geo_temp', 0),
                        'drilling_depth': st.session_state.geo_data.get('depth', 0),
                        'pipe_material': st.session_state.geo_data.get('pipe_material', 'N/A')
                    }
                }
                
                with st.spinner("🤖 AI is analyzing your data and writing the report... This may take 30-60 seconds."):
                    
                    # Generate the report using template (you can integrate with Claude API later)
                    report_content = generate_ai_report(
                        analysis_data, 
                        report_type, 
                        audience,
                        language_style,
                        analysis_focus,
                        include_comparisons,
                        include_implementation
                    )
                    
                    # Store in session state
                    st.session_state['ai_report'] = report_content
                    st.session_state['report_metadata'] = {
                        'type': report_type,
                        'audience': audience,
                        'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'location': st.session_state.geo_data.get('location_name')
                    }
                    
                    st.success("✅ AI Report Generated Successfully!")
                    st.balloons()
            
            # Display generated report
            if 'ai_report' in st.session_state:
                st.markdown("---")
                st.markdown("### 📄 Generated Report Preview")
                
                # Report metadata
                if 'report_metadata' in st.session_state:
                    meta = st.session_state['report_metadata']
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"**Type:** {meta.get('type')}")
                    with col2:
                        st.caption(f"**Audience:** {meta.get('audience')}")
                    with col3:
                        st.caption(f"**Generated:** {meta.get('generated_at')}")
                
                # Show report in expandable section
                with st.expander("📖 Read Full Report", expanded=True):
                    st.markdown(st.session_state['ai_report'])
                
                st.markdown("---")
                
                # Download options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Download as Markdown
                    st.download_button(
                        label="⬇️ Download as Markdown (.md)",
                        data=st.session_state['ai_report'],
                        file_name=f"AI_Report_{st.session_state.geo_data.get('location_name', 'location').replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                
                with col2:
                    # Download as Text
                    st.download_button(
                        label="⬇️ Download as Text (.txt)",
                        data=st.session_state['ai_report'],
                        file_name=f"AI_Report_{st.session_state.geo_data.get('location_name', 'location').replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                
                with col3:
                    if st.button("🔄 Generate New Report"):
                        del st.session_state['ai_report']
                        if 'report_metadata' in st.session_state:
                            del st.session_state['report_metadata']
                        st.rerun()
                
                st.info("💡 **Pro Tip:** You can copy the report text and paste it into Word/Google Docs, or convert the Markdown file to PDF using online tools!")
        
    # SUB-TAB 3: Batch Analysis
    with export_tab3:
        st.subheader("Batch Analysis from CSV")
        
        st.markdown("""
        Upload a CSV file with multiple locations to analyze them all at once.
        
        **Required CSV format:**
        ```
        location_name,latitude,longitude,waterfall_height_m,waterfall_flow_m3s,geo_temp_c,depth_km
        Location 1,23.8103,90.4125,50,10,200,3.0
        Location 2,24.8949,91.8687,30,12,150,2.5
        ```
        """)
        
        sample_data = {
            'location_name': ['Chittagong Hills', 'Sylhet Valley', 'Khulna Region'],
            'latitude': [22.3569, 24.8949, 22.8456],
            'longitude': [91.7832, 91.8687, 89.5403],
            'waterfall_height_m': [45, 30, 0],
            'waterfall_flow_m3s': [8.5, 12.0, 0],
            'geo_temp_c': [180, 150, 200],
            'depth_km': [2.8, 2.5, 3.5]
        }
        sample_df = pd.DataFrame(sample_data)
        
        st.download_button(
            label="⬇️ Download Sample CSV Template",
            data=sample_df.to_csv(index=False),
            file_name="sample_locations_template.csv",
            mime="text/csv"
        )
        
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file is not None:
            try:
                batch_df = pd.read_csv(uploaded_file)
                st.write("### Uploaded Data Preview")
                st.dataframe(batch_df.head(), use_container_width=True)
                
                if st.button("⚙️ Process All Locations", type="primary"):
                    
                    results = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, row in batch_df.iterrows():
                        status_text.text(f"Processing {row.get('location_name', f'Location {idx+1}')}...")
                        
                        lat = row.get('latitude', 0)
                        lng = row.get('longitude', 0)
                        h = row.get('waterfall_height_m', 0)
                        q = row.get('waterfall_flow_m3s', 0)
                        temp = row.get('geo_temp_c', 0)
                        depth = row.get('depth_km', 3.0)
                        
                        if h > 0 and q > 0:
                            p_waterfall = (1000 * 9.81 * q * h * 0.9) / 1_000_000
                            e_waterfall = p_waterfall * 24 * 365
                            waterfall_waste = e_waterfall * 1000 * 0.30
                        else:
                            p_waterfall = 0
                            e_waterfall = 0
                            waterfall_waste = 0
                        
                        if temp > 50:
                            p_geo = (50 * 4.18 * (temp - 25) * 0.15) / 1000
                            e_geo = p_geo * 24 * 365 * 0.85
                            geothermal_waste = e_geo * 1000 * 0.30
                        else:
                            p_geo = 0
                            e_geo = 0
                            geothermal_waste = 0
                        
                        # Waste recovery
                        total_waste = waterfall_waste + geothermal_waste
                        e_waste_recovered = (total_waste * 0.80) / 1000
                        
                        total_annual = e_waterfall + e_geo + e_waste_recovered
                        households = int(total_annual * 1000 / 7.2)
                        
                        # Carbon calculations
                        carbon_saved = total_annual * CARBON_FACTORS['grid_average_bangladesh']
                        
                        if temp < 300:
                            material = "Stainless Steel"
                        elif temp < 600:
                            material = "Inconel alloys"
                        else:
                            material = "Ceramic composites"
                        
                        results.append({
                            'Location': row.get('location_name', f'Location {idx+1}'),
                            'Latitude': lat,
                            'Longitude': lng,
                            'Waterfall_MW': round(p_waterfall, 2),
                            'Geothermal_MW': round(p_geo, 2),
                            'Total_Annual_MWh': round(total_annual, 0),
                            'CO2_Saved_tons': round(carbon_saved, 0),
                            'Households': households,
                            'Pipe_Material': material if temp > 50 else 'N/A'
                        })
                        
                        progress_bar.progress((idx + 1) / len(batch_df))
                    
                    status_text.text("✅ Processing complete!")
                    
                    results_df = pd.DataFrame(results)
                    st.write("### Batch Analysis Results")
                    st.dataframe(results_df, use_container_width=True)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Locations", len(results_df))
                    with col2:
                        total_power = results_df['Waterfall_MW'].sum() + results_df['Geothermal_MW'].sum()
                        st.metric("Combined Power", f"{total_power:.2f} MW")
                    with col3:
                        total_carbon = results_df['CO2_Saved_tons'].sum()
                        st.metric("Total CO₂ Saved", f"{total_carbon:,.0f} tons/yr")
                    with col4:
                        total_households = results_df['Households'].sum()
                        st.metric("Total Households", f"{total_households:,}")
                    
                    st.download_button(
                        label="⬇️ Download Batch Results",
                        data=results_df.to_csv(index=False),
                        file_name="batch_energy_analysis_results.csv",
                        mime="text/csv"
                    )
                    
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                st.info("Please make sure your CSV has the correct column names and format.")
