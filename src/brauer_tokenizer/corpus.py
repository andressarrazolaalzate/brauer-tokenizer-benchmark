"""Deterministic synthetic corpus used in the CIARP experiment."""
from __future__ import annotations
import hashlib
import random
from pathlib import Path

RANDOM_SEED = 20260823
N_SENTENCES = 500

SUBJECTS = [
    "The research assistant", "A small drone", "The library catalog", "Several engineers",
    "The medical team", "A quiet alarm", "The teacher", "Bright clouds", "The museum guide",
    "A delivery robot", "The software update", "A biologist", "The committee", "An architect",
    "The journalist", "A musician", "The weather station", "A mechanic", "The finance team",
    "A student", "The satellite image", "A laboratory notebook", "The customer service agent",
    "Several hikers", "The robotics club", "A public health campaign", "The gardener",
    "A historian", "The bicycle courier", "The chef", "A data analyst", "The park ranger",
    "A speech therapist", "The mathematics seminar", "A technician", "The court clerk",
    "Several neighbors", "The train conductor", "A product designer", "The astronomy club",
    "The conference volunteer", "The agricultural report", "A programmer", "The city council",
    "A nurse", "The composer", "A coastal sensor", "The student council", "A warehouse scanner",
    "The geologist", "A photographer", "The school cafeteria", "A legal assistant", "The marine biologist",
    "A coach", "The airport display", "A librarian", "The pharmacy technician", "A cartographer",
    "The security team", "A historian", "The physics class", "A community organizer", "The editor",
    "A civil engineer", "The pediatric clinic", "A logistics planner", "The chemistry student",
    "A museum archivist", "The emergency dispatcher", "A software tester", "The environmental agency",
    "A graduate student", "The bakery owner", "A surgeon", "The newspaper archive", "A language instructor",
    "The hiking group", "A network engineer", "The biology teacher", "A financial auditor",
    "The radio host", "The clinic receptionist", "A textile designer", "The traffic camera",
    "A database administrator", "The veterinarian", "A playwright", "The school principal",
    "A meteorologist", "The hardware team", "A translator", "The bakery window",
    "The city planner", "A researcher", "A graphic designer", "The classroom projector",
    "A public librarian", "The construction crew", "A physician", "The local orchestra",
    "A database query", "The health department", "A ceramic artist", "The grocery store",
    "A geography student", "The clinic manager", "The research group", "A firefighter",
    "The software dashboard", "The architecture studio", "A meteorological balloon",
    "The hospital cafeteria", "The conservation team", "A theater critic", "The warehouse robot",
    "A psychologist", "The electrical engineer", "A marine sensor", "The school newspaper",
    "The project manager", "A physicist", "The bus schedule", "The photography club",
    "A botanist", "The legal clinic", "A robotics student", "The water utility",
    "The hospital scheduler", "A data scientist", "The city library", "A structural engineer",
    "The language model tokenizer", "The environmental report", "A medical researcher",
    "The local Brauer model", "The tokenization pipeline", "The quiver diagram", "The graph algorithm"
]
VERBS = [
    "checked", "compared", "reviewed", "measured", "summarized", "updated", "verified",
    "recorded", "organized", "classified", "inspected", "calibrated", "translated", "reported",
    "estimated", "highlighted", "scheduled", "filtered", "mapped", "tested", "stored", "cleaned",
    "annotated", "repaired", "printed", "scanned", "counted", "displayed", "generated", "aligned",
    "explained", "monitored", "computed", "validated", "normalized", "clustered", "tokenized",
    "reconstructed", "selected", "documented", "evaluated", "archived", "revised", "simplified"
]
OBJECTS = [
    "the sensor log", "the prototype diagram", "the dosage chart", "the cooling system",
    "the classroom calculation", "the historical novel", "the route plan", "the user interface",
    "the greenhouse samples", "the safety notice", "the cardboard objects", "the vaccination schedule",
    "the census records", "the construction lanes", "the spreadsheet", "the trail map",
    "the pronunciation exercises", "the symmetry examples", "the microscope image", "the case numbers",
    "the registration list", "the soil moisture report", "the validation function", "the bike lane map",
    "the recovery plan", "the melody", "the wave-height measurements", "the shipping manifest",
    "the riverbed samples", "the theater photographs", "the contract deadlines", "the plankton species",
    "the match statistics", "the gate number", "the renewable energy articles", "the prescription record",
    "the regional planning map", "the authentication server", "the archive database", "the motion sensor data",
    "the volunteer schedule", "the article headline", "the bridge joints", "the appointment reminders",
    "the breakfast menu", "the rhythm pattern", "the highway report", "the titration reading",
    "the ceramic label", "the response address", "the installation profile", "the air quality readings",
    "the annotated sample", "the traffic patterns", "the imaging results", "the railway reports",
    "the stress patterns", "the weather forecast", "the packet losses", "the seasonal transitions",
    "the purchase orders", "the urban heat interview", "the perspective sketch", "the insurance forms",
    "the fabric collection", "the bus route", "the migration records", "the diagnostic tests",
    "the final scene", "the reading clubs", "the pressure readings", "the battery measurements",
    "the sentence structure", "the chemical samples", "the pedestrian flow", "the survey answers",
    "the mobile menu", "the academic database workshop", "the reinforcement grid", "the clinical notes",
    "the concert stream", "the join condition", "the infection statistics", "the supplier invoices",
    "the contour lines", "the bilingual glossary", "the seminar slides", "the training equipment",
    "the memory warnings", "the newspaper scans", "the facade model", "the temperature data",
    "the allergen labels", "the algorithmic operations", "the nesting area", "the performance review",
    "the pallet scanner", "the survey instructions", "the grounding connections", "the salinity measurements",
    "the alumni interviews", "the project timeline", "the simulated trajectories", "the software migration",
    "the street portraits", "the herbarium specimens", "the tenant guides", "the motor controller",
    "the water samples", "the trade route records", "the routine checkups", "the classifier features",
    "the weekend schedule", "the load combinations", "the subword units", "the recycling rates",
    "the transparent table", "the local incidence window", "the Brauer entropy values",
    "the co-occurrence graph", "the quiver arrows", "the tokenizer profile"
]
MODIFIERS = [
    "before the morning meeting", "after the supervisor requested clarification",
    "during the afternoon session", "while students asked follow-up questions",
    "because the first result looked unusual", "before the dashboard was published",
    "after the weekly report was reviewed", "while the team prepared the final summary",
    "before the next shift began", "after several measurements were repeated",
    "during the controlled experiment", "before the public demonstration",
    "after checking the reference file", "while the archive system was offline",
    "before the conference deadline", "after the route changed unexpectedly",
    "during the laboratory inspection", "before the model comparison was updated",
    "after the sensor produced a warning", "while the document was being revised"
]
SECOND_CLAUSES = [
    "and wrote a short note for the team.", "and stored the result in a transparent table.",
    "and compared the output with the previous version.", "and marked the unusual entries for later review.",
    "and added a timestamp to the final record.", "and explained the result in plain language.",
    "and sent the corrected file to the coordinator.", "and checked whether the pattern remained stable.",
    "and prepared a concise summary for the archive.", "and verified that every item matched the checklist.",
    "and reported a small change in the final indicator.", "and saved the examples for a second inspection.",
    "and attached the figures to the working folder.", "and noted how the local context changed.",
    "and confirmed that the labels were readable.", "and separated boundary cases from regular cases.",
    "and documented the assumptions used in the calculation.", "and preserved the original order of the observations.",
    "and highlighted the rows that needed attention.", "and reviewed the values before exporting the chart."
]
NUMERIC_TEMPLATES = [
    "{subject} {verb} {number} versions of {object} and reported a {percent} percent change in the summary.",
    "{subject} {verb} {object} for {number} separate cases before exporting the results.",
    "{subject} {verb} {object} at radius {radius} and compared it with radius {radius2}.",
    "{subject} {verb} {number} entries from {object} while preserving the original order.",
]


def generate_reference_corpus(seed: int = RANDOM_SEED, n_sentences: int = N_SENTENCES) -> list[str]:
    rng = random.Random(seed)
    sentences: set[str] = set()
    attempts = 0
    while len(sentences) < n_sentences and attempts < n_sentences * 100:
        attempts += 1
        subject, verb, obj = rng.choice(SUBJECTS), rng.choice(VERBS), rng.choice(OBJECTS)
        if rng.random() < 0.72:
            sentence = f"{subject} {verb} {obj} {rng.choice(MODIFIERS)}, {rng.choice(SECOND_CLAUSES)}"
        else:
            template = rng.choice(NUMERIC_TEMPLATES)
            r1 = rng.choice([0, 1, 2])
            r2 = rng.choice([r for r in [1, 2, 3] if r != r1])
            sentence = template.format(
                subject=subject, verb=verb, object=obj, number=rng.randint(3, 48),
                percent=rng.choice([5, 8, 12, 15, 20, 24, 30]), radius=r1, radius2=r2,
            )
        sentences.add(sentence)
    result = sorted(sentences)
    if len(result) != n_sentences:
        raise RuntimeError(f"generated {len(result)} unique sentences, expected {n_sentences}")
    return result


def corpus_text(sentences: list[str]) -> str:
    return "\n".join(sentences) + "\n"


def corpus_sha256(sentences: list[str]) -> str:
    return hashlib.sha256(corpus_text(sentences).encode("utf-8")).hexdigest()


def write_reference_corpus(path: str | Path) -> str:
    sentences = generate_reference_corpus()
    path = Path(path)
    path.write_text(corpus_text(sentences), encoding="utf-8")
    return corpus_sha256(sentences)


def validate_reference_corpus(path: str | Path) -> None:
    """Compare an existing file against a fresh deterministic regeneration."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    expected = corpus_text(generate_reference_corpus())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise ValueError("reference corpus does not match seed-20260823 regeneration")
