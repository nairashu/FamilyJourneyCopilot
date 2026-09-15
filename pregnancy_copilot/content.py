"""Educational content used by the Pregnancy Journey Copilot.

The content is intentionally general and educational. It never replaces advice
from a qualified healthcare professional.
"""

from __future__ import annotations

from typing import Dict, Tuple

from .models import Appointment, Guidance, NewbornStage, WeekMilestone

DISCLAIMER = (
    "Educational information only - not medical advice. Always follow the "
    "guidance of your midwife, obstetrician or paediatrician, and seek urgent "
    "care if something feels wrong."
)

GESTATION_DAYS = 280
FIRST_TRIMESTER_LAST_WEEK = 13
SECOND_TRIMESTER_LAST_WEEK = 27
LAST_WEEK = 40

_WEEK_ROWS: Tuple[Tuple[int, str, str, str], ...] = (
    (1, "Pregnancy is counted from the first day of the last period, so conception has not happened yet.",
     "You may be having your period; the body is preparing to release an egg.",
     "Start a prenatal vitamin with folic acid and note the first day of your last period."),
    (2, "Ovulation approaches and the uterine lining thickens.",
     "Fertile window begins; cervical mucus becomes clearer and stretchier.",
     "Track ovulation signs and keep alcohol and smoking out of the picture."),
    (3, "Fertilisation can occur and the single cell begins dividing on its way to the uterus.",
     "No outward symptoms yet; hormone levels are just starting to shift.",
     "Keep up folic acid and avoid unnecessary medication."),
    (4, "The blastocyst implants in the uterine wall and the placenta starts forming.",
     "A missed period and light implantation spotting are possible.",
     "Take a home pregnancy test and book a first appointment if positive."),
    (5, "The neural tube, which becomes brain and spinal cord, begins to close.",
     "Fatigue, tender breasts and frequent urination may appear.",
     "Confirm the pregnancy with your provider and review any current medication."),
    (6, "The heart starts beating and arm and leg buds appear.",
     "Morning sickness and heightened sense of smell often begin.",
     "Eat small frequent meals and stay hydrated."),
    (7, "The brain grows rapidly and the umbilical cord is fully formed.",
     "Nausea may peak; mood swings are common.",
     "Rest when you can and ask about vitamin B6 if nausea is hard to manage."),
    (8, "Fingers, toes and eyelids are forming; the baby is about the size of a raspberry.",
     "The uterus is expanding; bloating and cramping can occur.",
     "Attend the first prenatal visit and blood work."),
    (9, "Essential organs are in place and tiny muscles allow first movements.",
     "Breast changes continue and clothes may feel tighter.",
     "Discuss first-trimester screening options."),
    (10, "The embryo is now called a fetus; vital organs begin to function.",
     "Visible veins and mild dizziness are common.",
     "Consider non-invasive prenatal testing if offered."),
    (11, "Tooth buds form and the baby can hiccup.",
     "Nausea may start to ease; appetite can return.",
     "Plan the nuchal translucency ultrasound."),
    (12, "Reflexes develop and fingernails begin to grow.",
     "Risk of miscarriage drops noticeably; energy often improves.",
     "Many families share the news around now."),
    (13, "Vocal cords form and the baby's body grows faster than the head.",
     "The first trimester ends; a small bump may show.",
     "Review workplace rights and plan parental leave."),
    (14, "Facial muscles let the baby squint and frown; fine lanugo hair appears.",
     "The second trimester often brings more energy and less nausea.",
     "Return to gentle exercise such as walking or prenatal yoga."),
    (15, "Bones harden and the baby can sense light through the closed eyelids.",
     "Nasal congestion and mild swelling can occur.",
     "Keep iron-rich foods on the plate."),
    (16, "The baby may begin to hear your voice and heartbeat.",
     "Some people feel the first flutters of movement (quickening).",
     "Start talking and reading to the baby, partners included."),
    (17, "Fat stores start forming and the umbilical cord thickens.",
     "Round ligament pain and vivid dreams are common.",
     "Switch to sleeping on your side with a pillow for support."),
    (18, "Hearing is well developed and the digestive system practises swallowing.",
     "Backache and leg cramps may appear as the bump grows.",
     "Book the anatomy scan."),
    (19, "Vernix caseosa coats the skin for protection.",
     "Skin changes such as a linea nigra can appear.",
     "Stay hydrated and moisturise the growing belly."),
    (20, "Halfway point: the baby measures roughly 25 cm head to heel.",
     "Movements become more noticeable and regular.",
     "Attend the mid-pregnancy anatomy ultrasound."),
    (21, "Bone marrow starts making blood cells; taste buds develop.",
     "Increased appetite and occasional heartburn.",
     "Choose balanced snacks and keep meals smaller in the evening."),
    (22, "Grip develops and the baby responds to sound and touch.",
     "Stretch marks may show; feet can swell.",
     "Elevate legs and wear comfortable shoes."),
    (23, "Rapid weight gain begins; lungs prepare for breathing.",
     "Braxton Hicks practice contractions may start.",
     "Learn the difference between practice and true contractions."),
    (24, "Viability milestone: the lungs produce surfactant.",
     "The uterus reaches above the navel.",
     "Take the glucose screening test when scheduled."),
    (25, "Hair gets colour and texture; hands are fully formed.",
     "Haemorrhoids and constipation can appear.",
     "Increase fibre and fluids, and move gently every day."),
    (26, "Eyes open for the first time and blinking begins.",
     "Sleep can become harder to find.",
     "Build a calming bedtime routine."),
    (27, "Brain activity increases and breathing motions practise for birth.",
     "The second trimester closes; ribs may feel pressure.",
     "Start counting daily movement patterns."),
    (28, "The baby starts to dream (REM sleep) and gains fat steadily.",
     "Third trimester begins; shortness of breath is common.",
     "Move to appointments every two weeks and check Rh status."),
    (29, "Bones are fully developed but still soft; kicks are strong.",
     "Heartburn and fatigue may increase.",
     "Track fetal movements daily and report changes."),
    (30, "Fluid around the baby decreases as the baby takes more space.",
     "Balance changes and mood swings can return.",
     "Book childbirth and newborn care classes."),
    (31, "The baby can process information and signal sleep cycles.",
     "Braxton Hicks become more noticeable.",
     "Practise breathing and relaxation techniques."),
    (32, "The baby often settles head down; fingernails reach the fingertips.",
     "Colostrum may leak from the breasts.",
     "Prepare the hospital bag and birth preferences."),
    (33, "The immune system strengthens with antibodies from you.",
     "Swelling in hands and feet is common - report sudden swelling.",
     "Install and check the infant car seat."),
    (34, "Lungs are nearly mature and the baby gains about 200 g a week.",
     "Pelvic pressure increases.",
     "Confirm the birth plan and who will support you in labour."),
    (35, "Most organs are ready; brain development accelerates.",
     "Frequent urination returns as the baby drops.",
     "Discuss group B strep testing."),
    (36, "The baby is considered late preterm; weight gain continues.",
     "Lightening: breathing gets easier as the baby settles lower.",
     "Switch to weekly prenatal visits."),
    (37, "Early term: the baby practises sucking and breathing.",
     "Mucus plug may be released; nesting energy is common.",
     "Know the signs of labour and when to call."),
    (38, "The baby's head circumference matches the abdomen.",
     "Cramping and irregular contractions are common.",
     "Arrange transport to the birth place and support at home."),
    (39, "Full term: lungs and brain continue to mature.",
     "Water may break; contractions can become regular.",
     "Rest, eat well and stay alert for labour signs."),
    (40, "Due date week: the baby is ready to meet you.",
     "Cervical changes progress; labour can start any day.",
     "Discuss monitoring and induction options if the baby is late."),
)


def _trimester_for(week: int) -> int:
    if week <= FIRST_TRIMESTER_LAST_WEEK:
        return 1
    if week <= SECOND_TRIMESTER_LAST_WEEK:
        return 2
    return 3


WEEK_MILESTONES: Dict[int, WeekMilestone] = {
    row[0]: WeekMilestone(
        week=row[0],
        trimester=_trimester_for(row[0]),
        baby_development=row[1],
        mother_changes=row[2],
        focus=row[3],
    )
    for row in _WEEK_ROWS
}

GENERAL_GUIDANCE = Guidance(
    dos=(
        "Take a daily prenatal vitamin with folic acid and the iodine or iron your provider recommends.",
        "Attend every scheduled prenatal appointment and screening.",
        "Eat a varied diet with protein, whole grains, fruit and vegetables, and drink water regularly.",
        "Stay gently active with walking, swimming or prenatal yoga unless advised otherwise.",
        "Ask your provider before starting any medication, herbal remedy or supplement.",
    ),
    donts=(
        "Do not smoke, vape, or use recreational drugs, and avoid second-hand smoke.",
        "Do not drink alcohol - no amount is known to be safe in pregnancy.",
        "Do not eat raw or undercooked meat, fish or eggs, or unpasteurised dairy.",
        "Do not ignore warning signs such as heavy bleeding, severe headache, blurred vision or reduced fetal movement.",
        "Do not self-diagnose from unverified sources - bring questions to your care team.",
    ),
)

TRIMESTER_GUIDANCE: Dict[int, Guidance] = {
    1: Guidance(
        dos=(
            "Eat small, frequent meals to manage nausea and keep blood sugar steady.",
            "Rest early and often - first trimester fatigue is real.",
            "Confirm which of your current medications are safe to continue.",
        ),
        donts=(
            "Do not exceed about 200 mg of caffeine a day (roughly one strong coffee).",
            "Do not handle cat litter or garden soil without gloves (toxoplasmosis risk).",
            "Do not take high-dose vitamin A supplements or retinoid skin treatments.",
        ),
    ),
    2: Guidance(
        dos=(
            "Book the anatomy scan and glucose screening on time.",
            "Sleep on your side with a pillow between the knees.",
            "Start pelvic floor exercises and gentle strength work.",
        ),
        donts=(
            "Do not lie flat on your back for long periods after about week 20.",
            "Do not skip iron-rich foods - anaemia is common in this stage.",
            "Do not take on contact sports or activities with a fall risk.",
        ),
    ),
    3: Guidance(
        dos=(
            "Count fetal movements daily and call if the pattern changes.",
            "Pack the hospital bag and install the infant car seat by week 36.",
            "Write a flexible birth plan and share it with your support people.",
        ),
        donts=(
            "Do not ignore sudden swelling, severe headache or upper abdominal pain - they can signal pre-eclampsia.",
            "Do not travel far from your birth place after week 36 without medical advice.",
            "Do not lift heavy objects or stand for very long stretches.",
        ),
    ),
}

PARTNER_TIPS: Dict[int, Tuple[str, ...]] = {
    1: (
        "Learn the basics of the first trimester so symptoms do not take you by surprise.",
        "Take over tasks that trigger nausea, such as cooking strong-smelling food.",
        "Come along to the first appointment and write down the questions you both have.",
        "Protect rest time and quietly absorb chores in the evenings.",
        "Check in about worries - early pregnancy can feel uncertain for both of you.",
    ),
    2: (
        "Join the anatomy scan; it is a milestone worth sharing.",
        "Talk and read to the bump - the baby can hear you from around week 16.",
        "Help set up the nursery and compare practical baby gear together.",
        "Book a childbirth class and attend it as a team.",
        "Plan leave from work and how the first weeks at home will run.",
    ),
    3: (
        "Learn the signs of labour and rehearse the route to the birth place.",
        "Practise comfort measures: back pressure, breathing pacing, calm words.",
        "Keep the hospital bag, documents and car seat ready and accessible.",
        "Agree on who to call and what to share once the baby arrives.",
        "Plan meals and household support for the first two weeks postpartum.",
    ),
}

NEWBORN_GUIDANCE = Guidance(
    dos=(
        "Place the baby on their back to sleep, on a firm flat surface in your room.",
        "Feed on demand, roughly 8-12 times in 24 hours in the early weeks.",
        "Track wet and dirty nappies as a sign of enough feeding.",
        "Wash hands before handling the baby and support the head and neck.",
        "Share the load: alternate night shifts and accept offers of help.",
    ),
    donts=(
        "Do not put pillows, bumpers, loose blankets or soft toys in the sleep space.",
        "Do not give water, honey or solid food before the ages your provider advises.",
        "Do not shake the baby - put the baby down safely and take a break if overwhelmed.",
        "Do not smoke around the baby or let the baby overheat.",
        "Do not dismiss signs of postpartum depression in either parent - ask for help early.",
    ),
)

NEWBORN_STAGES: Tuple[NewbornStage, ...] = (
    NewbornStage(
        name="Golden hours (day 0)",
        start_day=0,
        end_day=0,
        highlights=(
            "Skin-to-skin contact regulates the baby's temperature, breathing and heart rate.",
            "First feed usually happens within the first hour.",
        ),
        care_tips=(
            "Keep the baby skin-to-skin as long as possible, partners included.",
            "Ask for feeding support before you leave the birth room.",
            "Expect vitamin K, newborn checks and first nappy of dark meconium.",
        ),
        warning_signs=(
            "Blue or grey colour around the lips or trouble breathing.",
            "Baby too sleepy to attempt any feed.",
        ),
    ),
    NewbornStage(
        name="First week (days 1-7)",
        start_day=1,
        end_day=7,
        highlights=(
            "Milk comes in around days 2-5 and cluster feeding is normal.",
            "Losing up to 7-10% of birth weight is expected, with recovery by about two weeks.",
        ),
        care_tips=(
            "Aim for 8-12 feeds in 24 hours and watch for 6+ wet nappies a day by day five.",
            "Keep the cord stump clean and dry; sponge bathe until it falls off.",
            "Sleep when the baby sleeps and limit visitors.",
        ),
        warning_signs=(
            "Fever of 38 C or higher - call immediately for a baby under three months.",
            "Deepening jaundice, refusal to feed, or fewer wet nappies than expected.",
        ),
    ),
    NewbornStage(
        name="Weeks 2-4",
        start_day=8,
        end_day=28,
        highlights=(
            "Alert periods lengthen and the baby starts tracking faces.",
            "Growth spurt around weeks 2-3 can mean more frequent feeding.",
        ),
        care_tips=(
            "Attend the newborn check and any hearing or metabolic screening.",
            "Start short tummy time sessions while the baby is awake and supervised.",
            "Take the postpartum mental health check seriously for both parents.",
        ),
        warning_signs=(
            "Persistent vomiting, dehydration, or no weight gain.",
            "Inconsolable crying that changes in pitch or pattern.",
        ),
    ),
    NewbornStage(
        name="Weeks 5-8",
        start_day=29,
        end_day=56,
        highlights=(
            "Social smiles usually appear around six weeks.",
            "Crying often peaks near six weeks before easing.",
        ),
        care_tips=(
            "Attend the six-week postnatal check for the birthing parent and the baby.",
            "Introduce a simple wind-down routine before night sleeps.",
            "Use the pause-and-breathe rule when crying feels overwhelming.",
        ),
        warning_signs=(
            "No response to sound or light, or floppy muscle tone.",
            "Feeding difficulties that stop weight gain.",
        ),
    ),
    NewbornStage(
        name="Months 3-4",
        start_day=57,
        end_day=120,
        highlights=(
            "Head control improves and the baby may roll or reach for objects.",
            "Longer night sleeps often begin, though regressions are normal.",
        ),
        care_tips=(
            "Keep vaccinations on schedule.",
            "Play face to face and narrate daily routines to build language.",
            "Revisit childcare, feeding and work plans as a family.",
        ),
        warning_signs=(
            "No head control while supported upright, or no social smiling.",
            "Loss of skills the baby previously had.",
        ),
    ),
)

APPOINTMENTS: Tuple[Appointment, ...] = (
    Appointment(8, "First prenatal visit", "Confirm pregnancy, dating scan, blood work and health history."),
    Appointment(12, "Nuchal translucency scan", "First-trimester screening for chromosomal conditions."),
    Appointment(16, "Routine check", "Blood pressure, weight, urine test and baby's heartbeat."),
    Appointment(20, "Anatomy ultrasound", "Detailed scan of the baby's organs, growth and placenta."),
    Appointment(24, "Glucose screening", "Test for gestational diabetes."),
    Appointment(28, "Third trimester start", "Rh antibody check, blood count and movement counting advice."),
    Appointment(32, "Growth check", "Fundal height, position and birth plan discussion."),
    Appointment(36, "Group B strep swab", "Screening plus weekly visits from now on."),
    Appointment(38, "Term check", "Position, cervix check and labour signs review."),
    Appointment(40, "Due date visit", "Monitoring and discussion of next steps if the baby is late."),
)

EMERGENCY_SIGNS: Tuple[str, ...] = (
    "Heavy vaginal bleeding or leaking fluid before week 37.",
    "Severe or persistent headache, blurred vision, or sudden swelling of face and hands.",
    "Severe abdominal pain or regular painful contractions before week 37.",
    "Noticeably reduced or absent fetal movement.",
    "Fever above 38 C, fainting, chest pain or difficulty breathing.",
)
