from src.glossary.service import GlossaryService
from src.glossary.models import GlossaryEntry

service = GlossaryService([GlossaryEntry("Force", "نیرو", case_sensitive=True), GlossaryEntry("John Wick", "جان ویک")])
assert [x.target for x in service.find_terms("The Force is strong.")] == ["نیرو"]
assert {x.target for x in service.find_terms("John Wick uses the Force.")} == {"جان ویک", "نیرو"}
assert service.find_terms("force of gravity") == []
print("glossary check passed")
