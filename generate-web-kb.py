"""
Transform progpol brain.json into web-optimized progpol-web-kb.json
"""
import json
from collections import defaultdict

BRAIN_PATH = "G:/My Drive/LIFE/brains/progpol/brain.json"
OUTPUT_PATH = "G:/My Drive/LIFE/projects/scovert.com/progpol/progpol-web-kb.json"

SECTIONS = [
    {
        "id": "democracy-under-attack",
        "title": "DEMOCRACY UNDER ATTACK",
        "subtitle": "Gerrymandering, voter suppression, electoral college distortion, filibuster abuse, and the systematic dismantling of democratic institutions.",
        "categories": ["democracy"],
        "narrative": "American democracy faces structural attacks on multiple fronts. Gerrymandering lets politicians choose their voters (North Carolina went from 10-3 to 7-6 after courts intervened). The Electoral College has installed 5 minority-vote presidents. The filibuster lets 1 senator block 99. Since 2011, over 1,688 voting restrictions have been introduced across 49 states. Project 2025 provides the blueprint for institutional capture. Understanding these mechanisms is the first step to defending against them.",
        "keyStats": [
            {"stat": "1,688", "label": "Voting restrictions introduced in 49 states since 2011"},
            {"stat": "5", "label": "Presidents who lost the popular vote but won the Electoral College"},
            {"stat": "38x", "label": "More criminal indictments for Republican vs Democratic administrations (1961-2016)"}
        ]
    },
    {
        "id": "economic-reality",
        "title": "ECONOMIC REALITY vs. ECONOMIC MYTHOLOGY",
        "subtitle": "Trickle-down debunked, wealth hoarding mechanics, corporate welfare, union busting, and the data on what actually grows economies.",
        "categories": ["economy", "labor"],
        "narrative": "A 50-year LSE study across 18 countries found zero evidence that tax cuts for the rich stimulate growth -- the only measurable effect was that the top 1%'s income share doubled. Meanwhile, corporate welfare costs $92B/year (vs $70B for the entire social safety net). Three Americans own more wealth than the bottom 50% combined. Piketty's r>g formula shows why: capital returns 4-5% while economic growth averages 1-1.5%, mathematically guaranteeing concentration. Progressive economic policies aren't ideology -- they're what the data supports.",
        "keyStats": [
            {"stat": "50 years", "label": "LSE study: zero growth benefit from tax cuts for the rich"},
            {"stat": "$92B/yr", "label": "Corporate welfare vs $70B for the social safety net"},
            {"stat": "r > g", "label": "Piketty: capital returns (4-5%) always outpace growth (1-1.5%)"}
        ]
    },
    {
        "id": "inequality-corporate-power",
        "title": "INEQUALITY & CORPORATE POWER",
        "subtitle": "Wealth concentration, regulatory capture, dark money, lobbying, media consolidation, and how corporations write their own rules.",
        "categories": ["inequality", "corporate-power"],
        "narrative": "Six corporations control 90% of US media. Koch networks spend $889M per election cycle. Leonard Leo's network captured 6 of 9 Supreme Court seats and 80% of Trump's appeals court judges. ALEC has pushed 2,900 model bills across all 50 states, with 600+ becoming law. Donors Trust launders $165M/year in untraceable dark money. The right-wing funding machine dwarfs progressive organizing -- partially because fewer scruples means fewer norms stopping them from breaching democratic guardrails.",
        "keyStats": [
            {"stat": "6 corps", "label": "Control 90% of all US media consumed"},
            {"stat": "$1.9B", "label": "Dark money in 2024 elections (OpenSecrets)"},
            {"stat": "6 of 9", "label": "Supreme Court seats captured by Leonard Leo's network"}
        ]
    },
    {
        "id": "culture-war-machine",
        "title": "THE CULTURE WAR MACHINE",
        "subtitle": "Manufactured outrage, wedge issues, moral panics, and how cultural grievance is weaponized to distract from economic policy.",
        "categories": ["culture-war"],
        "narrative": "Culture wars serve a specific political function: they redirect working-class anger away from economic policy and toward cultural scapegoats. The Southern Strategy pioneered this -- Lee Atwater explained it openly in 1981. Today's version uses trans rights, CRT, immigration, and 'woke' as triggers to activate tribal identity while tax cuts, deregulation, and corporate welfare pass unnoticed. The pattern is consistent: every culture war panic peaks during legislative sessions that benefit the donor class.",
        "keyStats": [
            {"stat": "1981", "label": "Lee Atwater explicitly described the Southern Strategy playbook"},
            {"stat": "100%", "label": "Of wedge issues share a pattern: distract from economic policy"},
            {"stat": "Fox News", "label": "Founded 1996 specifically to prevent another Nixon resignation"}
        ]
    },
    {
        "id": "projection-confession",
        "title": "EVERY ACCUSATION IS A CONFESSION",
        "subtitle": "The GOP projection pattern: anti-gay lawmakers caught gay, 'protect the children' advocates convicted of child crimes, Dark Triad psychology, and the data on who actually commits the crimes they accuse others of.",
        "categories": ["political-psychology", "historical-patterns"],
        "narrative": "From 1961-2016, Republican administrations produced 142 criminal indictments vs 2 for Democrats -- a 71:1 ratio. At least 11 prominent anti-gay Republican politicians were caught in gay scandals. Multiple 'protect the children' advocates -- including Dennis Hastert (Speaker of the House) -- were convicted of child sex crimes. This isn't coincidence: Dark Triad personality research shows sociopaths systematically assume others are as dishonest as they are, making projection their default communication strategy. The accusation reveals the accuser.",
        "keyStats": [
            {"stat": "142 vs 2", "label": "Criminal indictments: Republican vs Democratic administrations (1961-2016)"},
            {"stat": "11+", "label": "Anti-gay Republican politicians caught in gay scandals"},
            {"stat": "71:1", "label": "Ratio of GOP to Dem criminal indictments over 55 years"}
        ]
    },
    {
        "id": "media-information",
        "title": "MEDIA, MISINFORMATION & PROPAGANDA",
        "subtitle": "Media consolidation, Sinclair 'must-run' scripts, Fox News as political operation, social media manipulation, and the deception pipeline.",
        "categories": ["media-critique", "tech-policy"],
        "narrative": "In 1983, 50 companies controlled US media. Today it's 6. Sinclair Broadcasting requires local stations to air 'must-run' conservative segments that appear as local news. Fox News was founded explicitly as a political operation. Social media algorithms amplify outrage because engagement = revenue. The result: millions of Americans live in information ecosystems designed to produce specific political outcomes, not informed citizens. Understanding the pipeline from think tank to talking point to viral outrage is essential for progressive communication strategy.",
        "keyStats": [
            {"stat": "50 to 6", "label": "Media companies controlling US news (1983 vs today)"},
            {"stat": "193", "label": "Sinclair Broadcasting stations airing mandatory conservative segments"},
            {"stat": "500%", "label": "More engagement on outrage content vs factual reporting (social media)"}
        ]
    },
    {
        "id": "policy-wins",
        "title": "POLICY: WHAT ACTUALLY WORKS",
        "subtitle": "Healthcare, education, infrastructure, housing, climate -- the evidence base for progressive policy positions.",
        "categories": ["policy", "healthcare", "housing"],
        "narrative": "Universal healthcare systems cost 30-50% less per capita than the US system while delivering better outcomes. Countries with strong public education systems have higher economic mobility. Infrastructure investment returns $1.50-$2.20 for every dollar spent. The progressive policy platform isn't idealism -- it's what the data from every other developed nation shows actually works. The challenge isn't evidence; it's overcoming the multi-billion dollar messaging machine that argues otherwise.",
        "keyStats": [
            {"stat": "30-50%", "label": "Less per capita cost for universal healthcare vs US system"},
            {"stat": "$1.50-2.20", "label": "ROI for every dollar of infrastructure investment"},
            {"stat": "33 of 33", "label": "Developed nations with universal healthcare (US is the exception)"}
        ]
    },
    {
        "id": "global-authoritarianism",
        "title": "GLOBAL AUTHORITARIANISM & HISTORICAL PARALLELS",
        "subtitle": "Project 2025, Gleichschaltung parallels, democratic backsliding worldwide, Trump copycats, and what history tells us about this moment.",
        "categories": ["foreign-policy", "institutional-failure"],
        "narrative": "Project 2025 mirrors historical authoritarian consolidation playbooks. The Gleichschaltung comparison (Nazi coordination of institutions) isn't hyperbole -- it's structural analysis. Globally, democratic backsliding is accelerating: Hungary, Turkey, Brazil (under Bolsonaro), India, and the Philippines all followed similar patterns. Trump has spawned copycats -- Poilievre in Canada, Milei in Argentina. The tariff capitulation pattern shows smaller nations bowing to authoritarian economic pressure. History shows these patterns are recognizable, resistible, but only if recognized early enough.",
        "keyStats": [
            {"stat": "72%", "label": "Of world's population now lives in autocracies (V-Dem 2024)"},
            {"stat": "920", "label": "Project 2025 pages detailing institutional capture blueprint"},
            {"stat": "6", "label": "Major democracies that followed the same backsliding pattern in 10 years"}
        ]
    }
]

def main():
    with open(BRAIN_PATH, 'r', encoding='utf-8') as f:
        brain = json.load(f)

    entries_raw = brain['entries']
    print(f"Source entries: {len(entries_raw)}")

    # Build category -> section mapping
    cat_to_section = {}
    for section in SECTIONS:
        for cat in section['categories']:
            cat_to_section[cat] = section['id']

    # Transform entries
    entries = []
    topic_index = defaultdict(list)
    category_index = defaultdict(list)
    all_tags = set()

    for i, raw in enumerate(entries_raw):
        category = raw.get('category', 'other')
        section_id = cat_to_section.get(category, 'policy-wins')  # default to policy

        # Extract key facts as data points
        key_facts = raw.get('keyFacts', [])

        tags = raw.get('tags', [])
        for tag in tags:
            topic_index[tag].append(i)
            all_tags.add(tag)
        category_index[category].append(i)

        entry = {
            "id": i,
            "section": section_id,
            "source": raw.get('source', ''),
            "sourceType": raw.get('sourceType', ''),
            "category": category,
            "summary": raw.get('summary', ''),
            "keyFacts": key_facts[:8],  # Cap at 8 for web display
            "biasFlags": raw.get('biasFlags', []),
            "tags": tags,
            "url": raw.get('url', '')
        }
        entries.append(entry)

    # Assign entry IDs to sections
    for section in SECTIONS:
        section['entryIds'] = [e['id'] for e in entries if e['section'] == section['id']]

    # Build web KB
    from datetime import date
    web_kb = {
        "name": "progpol-web-kb",
        "version": "1.0.0",
        "generated": str(date.today()),
        "sourceEntries": len(entries),
        "stats": {
            "totalEntries": len(entries),
            "totalCategories": len(set(e['category'] for e in entries)),
            "totalTags": len(all_tags)
        },
        "framework": {
            "sections": [{
                "id": s['id'],
                "title": s['title'],
                "subtitle": s['subtitle'],
                "narrative": s['narrative'],
                "entryIds": s['entryIds'],
                "keyStats": s['keyStats']
            } for s in SECTIONS]
        },
        "entries": entries,
        "topicIndex": dict(topic_index),
        "categoryIndex": dict(category_index)
    }

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(web_kb, f, indent=2, ensure_ascii=False)

    print(f"Output: {len(entries)} entries in {len(SECTIONS)} sections")
    print(f"Tags: {len(all_tags)}, Categories: {web_kb['stats']['totalCategories']}")
    for s in SECTIONS:
        print(f"  {s['title']}: {len(s['entryIds'])} entries")

if __name__ == '__main__':
    main()
