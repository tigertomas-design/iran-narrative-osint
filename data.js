// ═══════════════════════════════════════════════════════════════════════════════
// OSINT DATABASE — רשתות נרטיב
// Iranian State Narrative Network Analysis — Jan 1 to Apr 24, 2026
// All data sourced from open-source journalism, OSINT reports, and verified archives.
// ═══════════════════════════════════════════════════════════════════════════════

// ── TRUMP POSTS ──────────────────────────────────────────────────────────────
// 40 verified entries, Jan 1 – Apr 24, 2026
// Sources: NPR, PBS, Al Jazeera, CNBC, CBS, Axios, WaPo, Time, etc.
// confidence: H = verbatim quote, multi-outlet; M = paraphrase / single outlet

const TRUMP_POSTS = [
  {
    id: "T001",
    date: "2026-01-02",
    platform: "Truth Social",
    time_approx: "02:58 ET",
    quote: "If Iran shots and violently kills peaceful protesters, which is their custom, the United States of America will come to their rescue. We are locked and loaded and ready to go.",
    topic: ["iran-protests", "military-threat"],
    narrative: "military-threat",
    aggression: 4,
    targets: ["Iran"],
    context: "Economic protests erupted Dec 28. Trump threatens US military intervention if protesters killed. Typo 'shots' for 'shoots' in original.",
    verified: true,
    confidence: "H",
    sources: ["cbsnews.com","foxnews.com","snopes.com","cnbc.com"]
  },
  {
    id: "T002",
    date: "2026-01-13",
    platform: "Truth Social",
    quote: "Iranian Patriots, KEEP PROTESTING - TAKE OVER YOUR INSTITUTIONS!!! Save the names of the killers and abusers. They will pay a big price. I have cancelled all meetings with Iranian Officials until the senseless killing of protesters STOPS. HELP IS ON ITS WAY.",
    topic: ["iran-protests", "regime-change"],
    narrative: "regime-change",
    aggression: 4,
    targets: ["Iran"],
    context: "~2,000 protesters killed in crackdown Jan 8-9. Trump cancels indirect contacts. Urges Iranians to seize government institutions.",
    verified: true,
    confidence: "H",
    sources: ["aljazeera.com","axios.com","iranintl.com","nbcnews.com"]
  },
  {
    id: "T003",
    date: "2026-02-04",
    platform: "NBC News interview",
    quote: "I would say he should be very worried, yeah. He should be.",
    topic: ["military-threat"],
    narrative: "military-threat",
    aggression: 3,
    targets: ["Khamenei"],
    context: "Asked about Khamenei ahead of US-Iran Oman talks. Iran wanted venue change from Turkey to Oman.",
    verified: true,
    confidence: "M",
    sources: ["bloomberg.com"]
  },
  {
    id: "T004",
    date: "2026-02-06",
    platform: "Press remarks",
    quote: "They can't have nuclear weapons. It's very simple. You can't have peace in the Middle East if they have a nuclear weapon.",
    topic: ["nuclear-threat"],
    narrative: "nuclear-threat",
    aggression: 3,
    targets: ["Iran"],
    context: "Day of first US-Iran indirect talks in Muscat, Oman, mediated by Omani FM Badr bin Hamad Al Busaidi.",
    verified: true,
    confidence: "M",
    sources: ["cnn.com","wikipedia.org"]
  },
  {
    id: "T005",
    date: "2026-02-19",
    platform: "Board of Peace meeting",
    quote: "I would think that will be enough time -- 10, 15 days, pretty much, maximum. You're going to be finding out over the next probably 10 days.",
    topic: ["nuclear-threat", "negotiations"],
    narrative: "nuclear-threat",
    aggression: 3,
    targets: ["Iran"],
    context: "Inaugural 'Board of Peace' meeting at US Institute of Peace. Khamenei rejected Trump's conditions Feb 17. Informal 10-15 day deadline issued.",
    verified: true,
    confidence: "H",
    sources: ["aljazeera.com","timesofisrael.com","foxnews.com"]
  },
  {
    id: "T006",
    date: "2026-02-27",
    platform: "Press remarks",
    quote: "I'm not happy with the fact that they're not willing to give us what we have to have. So I'm not thrilled.",
    topic: ["nuclear-threat", "negotiations"],
    narrative: "nuclear-threat",
    aggression: 3,
    targets: ["Iran"],
    context: "Final round of pre-war indirect talks. Oman FM said 'significant progress'; Trump said 'not thrilled.' Strike decision imminent.",
    verified: true,
    confidence: "H",
    sources: ["euronews.com","washingtonpost.com"]
  },
  {
    id: "T007",
    date: "2026-02-28",
    platform: "Truth Social (8-minute video)",
    quote: "A short time ago, the United States military began major combat operations in Iran. Our objective is to defend the American people by eliminating imminent threats from the Iranian regime... Bombs will be dropping everywhere... When we are finished, take over your government. It will be yours to take.",
    topic: ["military-threat", "nuclear-threat", "regime-change"],
    narrative: "military-threat",
    aggression: 5,
    targets: ["Iran"],
    context: "Launch of Operation Epic Fury — US-Israel joint strikes including assassination of Supreme Leader Khamenei. Posted before major outlets confirmed.",
    verified: true,
    confidence: "H",
    sources: ["pbs.org","cbsnews.com","axios.com","bostonglobe.com"]
  },
  {
    id: "T008",
    date: "2026-03-02",
    platform: "White House document",
    quote: "[White House document: '74 Times President Trump Has Made Clear That Iran Cannot Have a Nuclear Weapon']",
    topic: ["nuclear-threat"],
    narrative: "nuclear-threat",
    aggression: 3,
    targets: ["Iran"],
    context: "WH messaging doc released to reinforce justification for Operation Epic Fury.",
    verified: true,
    confidence: "H",
    sources: ["whitehouse.gov"]
  },
  {
    id: "T009",
    date: "2026-03-06",
    platform: "Truth Social + Axios interview",
    quote: "There will be no deal with Iran except UNCONDITIONAL SURRENDER! After that, and the selection of a GREAT & ACCEPTABLE Leader(s), we, and many of our wonderful and very brave allies and partners, will work tirelessly to bring Iran back from the brink of destruction, making it economically bigger, better, and stronger than ever before.",
    topic: ["military-threat", "regime-change"],
    narrative: "military-threat",
    aggression: 5,
    targets: ["Iran"],
    context: "One week into war. Iran firing back with missiles/drones. 'Unconditional surrender' = when Iran 'can't fight any longer.'",
    verified: true,
    confidence: "H",
    sources: ["aljazeera.com","axios.com","cnbc.com","cnn.com"]
  },
  {
    id: "T010",
    date: "2026-03-09",
    platform: "Press conference",
    quote: "We have sanctions on some countries. We're going to take sanctions off until this straightens out.",
    topic: ["sanctions"],
    narrative: "sanctions",
    aggression: 2,
    targets: ["Iran"],
    context: "Oil prices surged above $120/barrel. Trump suspending some oil sanctions to ease price pressure.",
    verified: true,
    confidence: "M",
    sources: ["aljazeera.com","spglobal.com"]
  },
  {
    id: "T011",
    date: "2026-03-13",
    platform: "Press remarks",
    quote: "[Regime change in Iran] will eventually happen... [but it] may not happen quickly under such conditions.",
    topic: ["regime-change"],
    narrative: "regime-change",
    aggression: 3,
    targets: ["Iran"],
    context: "Two weeks into war. Iran surviving. Trump walking back fast regime change rhetoric.",
    verified: true,
    confidence: "M",
    sources: ["iranintl.com"]
  },
  {
    id: "T012",
    date: "2026-03-21",
    platform: "Truth Social",
    quote: "If Iran doesn't FULLY OPEN, WITHOUT THREAT, the Strait of Hormuz, within 48 HOURS from this exact point in time, the United States of America will hit and obliterate their various POWER PLANTS, STARTING WITH THE BIGGEST ONE FIRST!",
    topic: ["hormuz", "military-threat"],
    narrative: "hormuz",
    aggression: 5,
    targets: ["Iran"],
    context: "Iran closed Strait of Hormuz in retaliation. First of multiple Hormuz ultimatums.",
    verified: true,
    confidence: "H",
    sources: ["npr.org","nbcnews.com","aljazeera.com"]
  },
  {
    id: "T013",
    date: "2026-03-23",
    platform: "Truth Social",
    quote: "I HAVE INSTRUCTED THE DEPARTMENT OF WAR TO POSTPONE ANY AND ALL MILITARY STRIKES AGAINST IRANIAN POWER PLANTS AND ENERGY INFRASTRUCTURE FOR A FIVE DAY PERIOD... They want to make a deal, and we are very willing to make a deal.",
    topic: ["negotiations", "military-threat"],
    narrative: "negotiations",
    aggression: 2,
    targets: ["Iran"],
    context: "Hours before March 23 deadline. Iran denied any talks. Oil prices dropped sharply on announcement.",
    verified: true,
    confidence: "H",
    sources: ["aljazeera.com","axios.com"]
  },
  {
    id: "T014",
    date: "2026-03-26",
    platform: "Truth Social",
    quote: "As per Iranian Government request, please let this statement serve to represent that I am pausing the period of Energy Plant destruction by 10 Days to Monday, April 6, 2026, at 8 P.M., Eastern Time.",
    topic: ["negotiations", "military-threat"],
    narrative: "negotiations",
    aggression: 2,
    targets: ["Iran"],
    context: "5-day pause expiring. Trump extends to April 6. Iran still denying talks.",
    verified: true,
    confidence: "H",
    sources: ["npr.org","aljazeera.com"]
  },
  {
    id: "T015",
    date: "2026-03-30",
    platform: "Truth Social",
    quote: "Great progress has been made but, if for any reason a deal is not shortly reached... we will conclude our lovely 'stay' in Iran by blowing up and completely obliterating all of their Electric Generating Plants, Oil Wells and Kharg Island (and possibly all desalinization plants!)",
    topic: ["hormuz", "military-threat"],
    narrative: "hormuz",
    aggression: 5,
    targets: ["Iran"],
    context: "Iran's proposal deemed 'unrealistic.' Iran struck US personnel in Saudi Arabia. Target list expanded.",
    verified: true,
    confidence: "H",
    sources: ["cnbc.com","aljazeera.com","axios.com"]
  },
  {
    id: "T016",
    date: "2026-04-01",
    platform: "Primetime national address",
    quote: "We are going to bring them back to the stone ages, where they belong... We are going to hit each and every one of their electric generating plants very hard, and probably simultaneously... [The war is] nearing completion.",
    topic: ["military-threat"],
    narrative: "military-threat",
    aggression: 5,
    targets: ["Iran"],
    context: "Day 33 of conflict. Oil above $100/barrel. Trump's first primetime Iran address.",
    verified: true,
    confidence: "H",
    sources: ["cnbc.com","millercenter.org","cnn.com"]
  },
  {
    id: "T017",
    date: "2026-04-05",
    platform: "Truth Social",
    time_approx: "~00:30 ET",
    quote: "WE GOT HIM! Over the past several hours, the United States Military pulled off one of the most daring Search and Rescue Operations in U.S. History. We have rescued the seriously wounded, and really brave, F-15 Crew Member/Officer, from deep inside the mountains of Iran.",
    topic: ["military-threat"],
    narrative: "military-threat",
    aggression: 3,
    targets: ["Iran"],
    context: "F-15E shot down April 3. Colonel rescued after 24+ hours behind enemy lines. Delta Force + SEAL Team 6.",
    verified: true,
    confidence: "H",
    sources: ["cbsnews.com","cnbc.com","yahoo.com"]
  },
  {
    id: "T018",
    date: "2026-04-05",
    platform: "Truth Social",
    time_approx: "Morning — Easter Sunday",
    quote: "Tuesday will be Power Plant Day, and Bridge Day, all wrapped up in one, in Iran. There will be nothing like it!!! Open the F***in' Strait, you crazy bastards, or you'll be living in Hell - JUST WATCH!",
    topic: ["hormuz", "military-threat"],
    narrative: "hormuz",
    aggression: 5,
    targets: ["Iran"],
    context: "Easter Sunday. This profane post DIRECTLY TRIGGERED the Iranian embassy 'Keys to Hormuz' mockery campaign.",
    verified: true,
    confidence: "H",
    sources: ["npr.org","washingtonpost.com","aljazeera.com"]
  },
  {
    id: "T019",
    date: "2026-04-06",
    platform: "Press conference",
    quote: "We are going to hit each and every one of their electric generating plants very hard, and probably simultaneously.",
    topic: ["military-threat", "hormuz"],
    narrative: "military-threat",
    aggression: 4,
    targets: ["Iran"],
    context: "Day before April 7 midnight deadline. Iran submitted 10-point peace plan Trump called 'not good enough.'",
    verified: true,
    confidence: "M",
    sources: ["npr.org"]
  },
  {
    id: "T020",
    date: "2026-04-07",
    platform: "Truth Social",
    time_approx: "Early morning",
    quote: "A whole civilisation will die tonight, never to be brought back again. I don't want that to happen, but it probably will. However, now that we have Complete and Total Regime Change, where different, smarter, and less radicalized minds prevail, maybe something revolutionarily wonderful can happen, WHO KNOWS?",
    topic: ["military-threat", "regime-change"],
    narrative: "military-threat",
    aggression: 5,
    targets: ["Iran"],
    context: "Midnight deadline for Hormuz ceasefire. Amnesty International called this 'a threat to commit genocide.' Pakistan's PM and Field Marshal Munir intervened. Ceasefire followed ~90 min before deadline.",
    verified: true,
    confidence: "H",
    sources: ["nbcnews.com","axios.com","aljazeera.com","truthsocial.com"],
    x_url: "https://truthsocial.com/@realDonaldTrump/posts/116363336033995961"
  },
  {
    id: "T021",
    date: "2026-04-07",
    platform: "Truth Social",
    time_approx: "~22:30 ET",
    quote: "Based on conversations with Prime Minister Shehbaz Sharif and Field Marshal Asim Munir, of Pakistan... I agree to suspend the bombing and attack of Iran for a period of two weeks. This will be a double sided CEASEFIRE!",
    topic: ["ceasefire", "hormuz", "negotiations"],
    narrative: "ceasefire",
    aggression: 2,
    targets: ["Iran"],
    context: "Pakistan-mediated ceasefire announced. Contingent on complete Hormuz reopening. Iran's 10-point plan called 'workable basis.'",
    verified: true,
    confidence: "H",
    sources: ["cnbc.com","aljazeera.com","nbcnews.com"]
  },
  {
    id: "T022",
    date: "2026-04-08",
    platform: "Truth Social",
    quote: "There will be no enrichment of Uranium, and the United States will, working with Iran, dig up and remove all of the deeply buried (B-2 Bombers) Nuclear 'Dust.'",
    topic: ["nuclear-threat", "ceasefire"],
    narrative: "nuclear-threat",
    aggression: 2,
    targets: ["Iran"],
    context: "Day after ceasefire. Trump declaring zero enrichment as condition. Iran contradicted this within hours.",
    verified: true,
    confidence: "H",
    sources: ["stripes.com","thehill.com"]
  },
  {
    id: "T023",
    date: "2026-04-12",
    platform: "Truth Social",
    quote: "Effective immediately, the United States Navy, the Finest in the World, will begin the process of BLOCKADING any and all Ships trying to enter, or leave, the Strait of Hormuz... Any Iranian who fires at us, or at peaceful vessels, will be BLOWN TO HELL!",
    topic: ["hormuz", "military-threat"],
    narrative: "hormuz",
    aggression: 5,
    targets: ["Iran"],
    context: "Islamabad talks collapsed. Iran refused to abandon enrichment. Naval blockade ordered immediately.",
    verified: true,
    confidence: "H",
    sources: ["cnbc.com","aljazeera.com","cbsnews.com","time.com"]
  },
  {
    id: "T024",
    date: "2026-04-13",
    platform: "Truth Social",
    quote: "If any of these ships come anywhere close to our BLOCKADE, they will be immediately ELIMINATED, using the same system of kill that we use against the drug dealers on boats at Sea. It is quick and brutal.",
    topic: ["hormuz", "military-threat"],
    narrative: "hormuz",
    aggression: 5,
    targets: ["Iran"],
    context: "Blockade took effect April 13 at 10:00 a.m. ET under Admiral Brad Cooper at CENTCOM.",
    verified: true,
    confidence: "H",
    sources: ["cnbc.com","npr.org"]
  },
  {
    id: "T025",
    date: "2026-04-16",
    platform: "White House remarks",
    quote: "Iran has agreed very powerfully that it would not develop a nuclear weapon, agreeing to give us back the nuclear dust that's way underground because of the attack we made with the B2 bombers.",
    topic: ["nuclear-threat", "negotiations"],
    narrative: "nuclear-threat",
    aggression: 2,
    targets: ["Iran"],
    context: "Premature public claims about nuclear progress. Iran's FM immediately denied, said 'enriched uranium is as sacred as Iranian soil.'",
    verified: true,
    confidence: "H",
    sources: ["washingtonpost.com","newsweek.com"]
  },
  {
    id: "T026",
    date: "2026-04-17",
    platform: "CBS News phone interview",
    quote: "They agreed to everything... they will work with us to remove their enriched uranium.",
    topic: ["nuclear-threat", "negotiations"],
    narrative: "negotiations",
    aggression: 2,
    targets: ["Iran"],
    context: "Iran FM Baghaei: 'Enriched uranium is as sacred to us as Iranian soil and will not be transferred anywhere.' Significant contradiction.",
    verified: true,
    confidence: "H",
    sources: ["cbsnews.com"]
  },
  {
    id: "T027",
    date: "2026-04-19",
    platform: "Truth Social",
    quote: "Iran decided to fire bullets yesterday in the Strait of Hormuz — A Total Violation of our Ceasefire Agreement!",
    topic: ["ceasefire", "hormuz"],
    narrative: "ceasefire",
    aggression: 4,
    targets: ["Iran"],
    context: "Iranian forces fired on commercial vessels. TOUSKA cargo ship seizure imminent.",
    verified: true,
    confidence: "H",
    sources: ["time.com"]
  },
  {
    id: "T028",
    date: "2026-04-19",
    platform: "Truth Social",
    quote: "Today, an Iranian-flagged cargo ship named TOUSKA, nearly 900 feet long and weighing almost as much as an aircraft carrier, tried to get past our Naval Blockade, and it did not go well for them. The U.S. Navy Guided Missile Destroyer USS SPRUANCE intercepted the TOUSKA in the Gulf of Oman, and gave them fair warning to stop. The Iranian crew refused to listen, so our Navy ship stopped them right in their tracks by blowing a hole in the engineroom.",
    topic: ["hormuz", "military-threat"],
    narrative: "hormuz",
    aggression: 4,
    targets: ["Iran"],
    context: "USS Spruance fired into engine room after 6-hour standoff. Iran called it 'piracy.' Major ceasefire escalation.",
    verified: true,
    confidence: "H",
    sources: ["cnbc.com","aljazeera.com"]
  },
  {
    id: "T029",
    date: "2026-04-20",
    platform: "Truth Social",
    quote: "Israel never talked me into the war with Iran. The results of Oct. 7th, added to my lifelong opinion that IRAN CAN NEVER HAVE A NUCLEAR WEAPON, did.",
    topic: ["nuclear-threat", "pro-israel"],
    narrative: "pro-israel",
    aggression: 3,
    targets: ["Israel", "Iran"],
    context: "WSJ and others reported Netanyahu lobbied Trump into war. Right-wing criticism of war's length growing.",
    verified: true,
    confidence: "H",
    sources: ["aljazeera.com","timesofisrael.com","axios.com"]
  },
  {
    id: "T030",
    date: "2026-04-20",
    platform: "Truth Social",
    quote: "The Anti-America Fake News Media is rooting for Iran to win, but it's not going to happen, because I'm in charge!",
    topic: ["domestic-politics"],
    narrative: "military-threat",
    aggression: 3,
    targets: ["Media"],
    context: "Part of 900+ word Truth Social posting spree on April 20.",
    verified: true,
    confidence: "H",
    sources: ["axios.com","washingtonexaminer.com"]
  },
  {
    id: "T031",
    date: "2026-04-20",
    platform: "Truth Social",
    quote: "The DEAL that we are making with Iran will be FAR BETTER than the JCPOA, commonly referred to as 'The Iran Nuclear Deal,' penned by Barack Hussein Obama and Sleepy Joe Biden, one of the Worst Deals ever made.",
    topic: ["nuclear-threat", "negotiations"],
    narrative: "nuclear-threat",
    aggression: 3,
    targets: ["Iran", "Obama"],
    context: "Comparing new negotiations favorably to JCPOA ahead of Islamabad talks.",
    verified: true,
    confidence: "H",
    sources: ["trump.news-pravda.com","timesofisrael.com"]
  },
  {
    id: "T032",
    date: "2026-04-20",
    platform: "Truth Social",
    quote: "I am under no pressure whatsoever, although, it will all happen, relatively quickly!",
    topic: ["negotiations"],
    narrative: "negotiations",
    aggression: 2,
    targets: ["Iran"],
    context: "War nearly 2 months old. Responding to criticism about ceasefire stalling.",
    verified: true,
    confidence: "H",
    sources: ["cnbc.com"]
  },
  {
    id: "T033",
    date: "2026-04-21",
    platform: "Truth Social",
    quote: "Based on the fact that the Government of Iran is seriously fractured... I have therefore directed our Military to continue the Blockade and, in all other respects, remain ready and able, and will therefore extend the Ceasefire until such time as their proposal is submitted.",
    topic: ["ceasefire", "negotiations"],
    narrative: "ceasefire",
    aggression: 2,
    targets: ["Iran"],
    context: "Iran's IRGC and civilian negotiators openly at odds. Mojtaba Khamenei barely communicating. Pakistan mediating.",
    verified: true,
    confidence: "H",
    sources: ["cnbc.com","aljazeera.com","time.com"]
  },
  {
    id: "T034",
    date: "2026-04-22",
    platform: "Truth Social",
    quote: "Iran doesn't want the Strait of Hormuz closed, they want it open so they can make $500 Million Dollars a day. They only say they want it closed because I have it totally BLOCKADED (CLOSED!), so they merely want to save face.",
    topic: ["hormuz", "sanctions"],
    narrative: "hormuz",
    aggression: 3,
    targets: ["Iran"],
    context: "Iran fired on 3 ships and seized two cargo ships. Ceasefire fraying.",
    verified: true,
    confidence: "H",
    sources: ["tribuneindia.com","cnbc.com"]
  },
  {
    id: "T035",
    date: "2026-04-22",
    platform: "Truth Social",
    quote: "Iran is collapsing financially! They want the Strait of Hormuz opened immediately — Starving for cash! Losing 500 Million Dollars a day... SOS!!!",
    topic: ["sanctions", "hormuz"],
    narrative: "sanctions",
    aggression: 3,
    targets: ["Iran"],
    context: "Iran's economy severely strained by blockade. Trump taunting.",
    verified: true,
    confidence: "H",
    sources: ["trump.news-pravda.com"]
  },
  {
    id: "T036",
    date: "2026-04-22",
    platform: "Truth Social",
    quote: "Iran's Navy is lying at the bottom of the Sea, their Air Force is demolished, their Anti Aircraft and Radar Weaponry is gone, their leaders are no longer with us, the Blockade is airtight and strong and, from there, it only gets worse — Time is not on their side!",
    topic: ["military-threat"],
    narrative: "military-threat",
    aggression: 4,
    targets: ["Iran"],
    context: "Response to WSJ editorial calling him a 'sucker' on Iran. Also called editor a 'moron.'",
    verified: true,
    confidence: "H",
    sources: ["thehill.com","rawstory.com"]
  },
  {
    id: "T037",
    date: "2026-04-23",
    platform: "Truth Social",
    quote: "I have ordered the United States Navy to shoot and kill any boat, small boats though they may be (Their naval ships are ALL, 159 of them, at the bottom of the sea!), that is putting mines in the waters of the Strait of Hormuz. There is to be no hesitation.",
    topic: ["hormuz", "military-threat"],
    narrative: "hormuz",
    aggression: 5,
    targets: ["Iran"],
    context: "IRGC deployed more mines in Hormuz. Third carrier strike group arrived. Mine-sweeping underway.",
    verified: true,
    confidence: "H",
    sources: ["cnbc.com","aljazeera.com","time.com"]
  },
  {
    id: "T038",
    date: "2026-04-23",
    platform: "Truth Social",
    quote: "I have all the time in the World, but Iran doesn't — The clock is ticking!",
    topic: ["negotiations", "sanctions"],
    narrative: "negotiations",
    aggression: 3,
    targets: ["Iran"],
    context: "Same day as mine-shooting order. Said to reporters: 'Don't rush me.'",
    verified: true,
    confidence: "H",
    sources: ["cnn.com"]
  },
  {
    id: "T039",
    date: "2026-04-23",
    platform: "Oval Office — remarks to reporters",
    quote: "Why would a stupid question like that be asked? Why would I use a nuclear weapon where we've totally in a very conventional way decimated them without it. A nuclear weapon should never be allowed to be used by anybody.",
    topic: ["nuclear-threat"],
    narrative: "nuclear-threat",
    aggression: 1,
    targets: ["Iran"],
    context: "Asked by PBS reporter Liz Landers. Bulletin of the Atomic Scientists had raised the nuclear weapons question.",
    verified: true,
    confidence: "H",
    sources: ["washingtontimes.com","pbs.org","newsweek.com"]
  },
  {
    id: "T040",
    date: "2026-04-23",
    platform: "Truth Social",
    quote: "I am possibly the least pressured person ever to be in this position. I am possibly the least pressured person ever to be in this position.",
    topic: ["negotiations"],
    narrative: "negotiations",
    aggression: 2,
    targets: ["Iran"],
    context: "Officials told CNN his posts were 'detrimental' to negotiations. Bloomberg: advisers divided on his social media blitz.",
    verified: true,
    confidence: "H",
    sources: ["fortune.com","bloomberg.com"]
  }
];

// ── KEY EVENTS TIMELINE ───────────────────────────────────────────────────────
const KEY_EVENTS = [
  { date: "2026-01-02", label: "Locked and loaded", desc: "Trump threatens military intervention in Iranian protests", type: "political" },
  { date: "2026-01-13", label: "Take over your institutions", desc: "Trump cancels Iran meetings, urges protesters to seize government", type: "political" },
  { date: "2026-02-06", label: "Oman talks begin", desc: "First US-Iran indirect talks in Muscat, Oman", type: "diplomatic" },
  { date: "2026-02-28", label: "Operation Epic Fury", desc: "US-Israel joint strikes launched; Khamenei killed; Hormuz closed", type: "military" },
  { date: "2026-03-02", label: "Hormuz closure", desc: "IRGC confirms full strait closure; ~20% global oil export affected", type: "military" },
  { date: "2026-03-06", label: "Unconditional surrender", desc: "Trump demands no deal except 'unconditional surrender'", type: "turning-point" },
  { date: "2026-03-08", label: "Mojtaba elected", desc: "Mojtaba Khamenei elected Supreme Leader", type: "political" },
  { date: "2026-03-21", label: "48-hr Hormuz ultimatum", desc: "Trump: open Hormuz or power plants obliterated", type: "turning-point" },
  { date: "2026-04-01", label: "Stone ages speech", desc: "Trump primetime address — 'bring them back to the stone ages'", type: "political" },
  { date: "2026-04-05", label: "F-15 rescue + Easter rant", desc: "Colonel rescued; Trump's profane Easter post triggers meme war", type: "incident" },
  { date: "2026-04-07", label: "Civilization will die", desc: "Trump: 'A whole civilisation will die tonight' — ceasefire follows", type: "turning-point" },
  { date: "2026-04-08", label: "Ceasefire", desc: "Two-week US-Iran ceasefire brokered by Pakistan", type: "diplomatic" },
  { date: "2026-04-12", label: "Naval blockade", desc: "Islamabad talks collapse; Trump orders Hormuz blockade", type: "military" },
  { date: "2026-04-19", label: "TOUSKA seizure", desc: "USS Spruance fires into engine room of Iranian cargo ship", type: "incident" },
  { date: "2026-04-22", label: "Firing on ships", desc: "Iran attacks 3+ commercial vessels; ceasefire near collapse", type: "military" },
  { date: "2026-04-23", label: "Shoot and kill mines", desc: "Trump orders Navy to kill any boat laying Hormuz mines", type: "military" }
];

// ── COORDINATED CAMPAIGNS ─────────────────────────────────────────────────────
const CAMPAIGNS = {
  "keys_to_hormuz": {
    label: "Keys to Hormuz / מפתחות הורמוז",
    trigger_post: "T018",
    trigger_date: "2026-04-05",
    dates: ["2026-04-05", "2026-04-06", "2026-04-07", "2026-04-08"],
    coordination_type: "Reply-thread cascade",
    accounts_confirmed: ["@IraninZimbabwe", "@IraninSA", "@IRANinBULGARIA"],
    accounts_likely: ["@Iran_in_UK", "@EmbassyofIrtoRF", "@IRANinTJ", "@IraninAlgeria", "@IRANinKENYA"],
    core_posts: [
      { account: "@IraninZimbabwe", date: "2026-04-05", text: "We've lost the keys.", views: 6900000, likes: 93000, x_url: "https://x.com/IRANinZIMBABWE/status/2041666510238650422" },
      { account: "@IraninSA",       date: "2026-04-05", text: "Shh… the key's under the flowerpot. Just open for friends.", views: null, likes: null },
      { account: "@IRANinBULGARIA", date: "2026-04-05", text: "Doors open for friends. Epstein's friends need keys.", views: null, likes: null },
      { account: "@IraninZimbabwe", date: "2026-04-07", text: "We found the keys.", views: 1900000, likes: null, x_url: "https://x.com/IRANinZIMBABWE/status/2041666510238650422" }
    ],
    strategy: ["Reframe Hormuz from capitulation to defiance", "Seed doubt about Trump credibility", "Global South solidarity signal", "Demonstrate regime survival post-Khamenei killing"]
  },
  "pirates_of_hormuz": {
    label: "Pirates of Hormuz",
    dates: ["2026-04-13", "2026-04-14", "2026-04-15", "2026-04-16"],
    coordination_type: "AI-generated visual content",
    accounts_confirmed: ["@IraninSA"],
    core_posts: [
      { account: "@IraninSA", date: "2026-04-13", text: "AI-generated: Trump, Vance, Hegseth as pirates — 'The miserable pirates of the Persian Gulf'", views: 3100000, likes: null }
    ]
  },
  "africa_iw": {
    label: "Africa Information Warfare Campaign",
    dates_range: ["2026-02-28", "2026-04-24"],
    coordination_type: "Geographic bloc campaign",
    accounts_confirmed: ["@IraninZimbabwe", "@IraninSA", "@IRANinKENYA", "@IRANinETHIOPIA", "@IraninAlgeria", "@IranNigeria"],
    strategy: ["Global South framing — Iran as underdog vs US imperialism", "Africa as swing audience", "English-language content despite local languages available"]
  }
};

// ── INAUTHENTIC AMPLIFICATION NETWORKS ───────────────────────────────────────
const INAUTHENTIC_NETWORKS = {
  "brics4clicks": {
    label: "BRICS4CLICKS",
    source: "ISD Global research",
    account_count: 23,
    total_views: "772M+",
    activation_date: "2026-02-28",
    notes: "Pivoted from Western-division to pro-Iran war propaganda within 24h of Operation Epic Fury. Amplified by Russian and Iranian diplomats. Blue checkmarks purchased Feb-Mar 2026."
  },
  "verified4war": {
    label: "Verified4War",
    source: "ISD Global research",
    account_count: 18,
    total_views: "370M+",
    blue_checkmarks_pct: 82,
    geographic_cluster: "South Asia / Southeast Asia",
    activation_date: "2026-02-28",
    notes: "14/18 accounts based South Asia/SE Asia. Connected via 'Iran Android App'. Username changes March 2026."
  },
  "clemson_fake_accounts": {
    label: "From Texas to Tehran (Clemson University report)",
    source: "Clemson University / DFRLab",
    account_count: 61,
    breakdown: {
      "fake_latina_US": 13,
      "fake_british_isles": 34,
      "fake_other": 14
    },
    geolocation: "Europe/France/UK (despite US/Latin America claimed identities)",
    notes: "AI-generated profile images. Connected via 'Iran Android App' metadata. Designed to look like organic US/Western voices."
  }
};

// ── HEBREW INFLUENCE OPERATIONS ───────────────────────────────────────────────
// Note: Hebrew ops run via Telegram/dedicated sites, NOT embassy X accounts
const HEBREW_OPS = [
  { type: "PressTV Hebrew Telegram", launched: "2025-12-01", platform: "Telegram", content: "Articles portraying Israel as economically weak, socially fragmented, politically corrupt", confidence: "H", source: "Ynet News" },
  { type: "IRGC Hebrew social media post", date: "2026-03-20", platform: "X/Telegram", content: "'We know all your secrets now'", confidence: "H", source: "Israel Hayom" },
  { type: "AI-generated Hebrew propaganda film", date: "2026-03-xx", platform: "Telegram", content: "Claims to present 'truth of the battlefield'; 44% infrastructure damage, 39% explosions; false claims about Fordow explosion", confidence: "H", source: "Times of Israel" },
  { type: "Fake Israeli social media impersonation", date_range: ["2026-02-28", "2026-04-24"], platform: "X/Telegram", content: "160% surge in foreign influence activity. Messages designed to deepen Israeli societal divisions.", confidence: "H", source: "Ynet News" },
  { type: "AI missile strike misinformation", date: "2026-03-xx", platform: "Telegram/X", content: "False claims of Iranian missiles striking Azrieli Towers in Tel Aviv", confidence: "H", source: "Jerusalem Post, Times of Israel" }
];

// ── ACCOUNTS DATABASE ─────────────────────────────────────────────────────────
// Each account: id, tier, type, platform, country, region, lang, conf, status, notes
// status: active / inactive / suspended / restricted
const ACCOUNTS = [

  // TIER 1 — Supreme Leadership
  { id: "@khamenei_ir",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "H", status: "inactive", notes: "Ali Khamenei killed Feb 28 2026 in Operation Epic Fury. Account archived." },
  { id: "@Khamenei_fa",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Global", lang: "FA", conf: "H", status: "inactive", notes: "Persian account — inactive since Feb 28 2026" },
  { id: "@ar_Khamenei",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Global", lang: "AR", conf: "H", status: "inactive", notes: "Arabic account — inactive since Feb 28 2026" },
  { id: "@Khamenei_es",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "LatAm", lang: "ES", conf: "M", status: "inactive", notes: "Spanish — inactive since Feb 28 2026" },
  { id: "@fr_Khamenei",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Europe", lang: "FR", conf: "H", status: "inactive", notes: "French — inactive since Feb 28 2026" },
  { id: "@Khamenei_fra",  tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Europe", lang: "FR", conf: "H", status: "inactive", notes: "French secondary — inactive since Feb 28 2026" },
  { id: "@de_Khamenei",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Europe", lang: "DE", conf: "M", status: "inactive", notes: "German — inactive since Feb 28 2026" },
  { id: "@it_Khamenei",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Europe", lang: "IT", conf: "M", status: "inactive", notes: "Italian — inactive since Feb 28 2026" },
  { id: "@tr_Khamenei_ir",tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Middle East", lang: "TR", conf: "M", status: "inactive", notes: "Turkish — inactive since Feb 28 2026" },
  { id: "@ur_Khamenei",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "South Asia", lang: "UR", conf: "M", status: "inactive", notes: "Urdu — inactive since Feb 28 2026" },
  { id: "@ru_Khamenei",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Europe", lang: "RU", conf: "M", status: "inactive", notes: "Russian — inactive since Feb 28 2026" },
  { id: "@in_Khamenei",   tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "South Asia", lang: "HI", conf: "M", status: "inactive", notes: "Hindi/Indonesian — inactive since Feb 28 2026" },
  { id: "@Khamenei_m",    tier: "T1", type: "leadership", platform: "X", country: "Iran", region: "Global", lang: "multi", conf: "M", status: "inactive", notes: "Multilingual — inactive since Feb 28 2026" },

  // TIER 2 — Iranian Government
  { id: "@araghchi",      tier: "T2", type: "government", platform: "X", country: "Iran", region: "Global", lang: "EN/FA", conf: "H", status: "active", notes: "Foreign Minister. Coined 'Operation Epic Mistake.' Attacked by Tasnim/IRGC Apr 16 over Hormuz tweet." },
  { id: "@drpezeshkian",  tier: "T2", type: "government", platform: "X", country: "Iran", region: "Global", lang: "EN/FA", conf: "H", status: "active", notes: "President. '6,000-year civilization' post widely cited." },
  { id: "@Iran_GOV",      tier: "T2", type: "government", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "H", status: "active", notes: "Official government. NPT Article 4 framing." },
  { id: "@IRIMFA_EN",     tier: "T2", type: "government", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "H", status: "active", notes: "Foreign Ministry English. Official statement relay." },
  { id: "@IRIMFA_SPOX",   tier: "T2", type: "government", platform: "X", country: "Iran", region: "Global", lang: "EN/FA", conf: "H", status: "active", notes: "MFA spokesperson Nasser Kanani." },
  { id: "@IRIran_Military",tier:"T2", type: "government", platform: "X", country: "Iran", region: "Global", lang: "EN/FA", conf: "H", status: "active", notes: "Military account. Ghalibaf missile capability statements." },
  { id: "@Iran_UN",       tier: "T2", type: "government", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "H", status: "active", notes: "Iran mission to UN. Legal framing (Article 51, Article 2(4))." },
  { id: "@IranmissionEU", tier: "T2", type: "government", platform: "X", country: "Iran", region: "Europe", lang: "EN", conf: "H", status: "active", notes: "Iran mission to EU. Brussels." },
  { id: "@PMIRAN_GENEVA", tier: "T2", type: "government", platform: "X", country: "Iran", region: "Europe", lang: "EN/FR", conf: "M", status: "active", notes: "Iran permanent mission Geneva (IAEA/UN)." },

  // TIER 3 — Embassies (HIGH ACTIVITY)
  { id: "@IraninZimbabwe",tier: "T3", type: "embassy", platform: "X", country: "Zimbabwe", region: "Africa", lang: "EN", conf: "H", status: "active", notes: "MOST VIRAL — 'We've lost the keys' (6.9M views). Lead seeder of Keys to Hormuz campaign." },
  { id: "@IraninSA",      tier: "T3", type: "embassy", platform: "X", country: "South Africa", region: "Africa", lang: "EN", conf: "H", status: "active", notes: "100K+ followers. 'Key under flowerpot.' Pirates meme. Antisemitic rat/kippah post (not suspended). Most prolific meme account." },
  { id: "@IRANinBULGARIA",tier: "T3", type: "embassy", platform: "X", country: "Bulgaria", region: "Europe", lang: "EN/BG", conf: "H", status: "active", notes: "'Epstein's friends need keys.' Keys to Hormuz thread." },
  { id: "@Iran_in_India", tier: "T3", type: "embassy", platform: "X", country: "India", region: "South Asia", lang: "EN", conf: "H", status: "active", notes: "Deleted Kashmir tweets under pressure — diplomatic incident India/Pakistan/Iran." },
  { id: "@IraninBerlin",  tier: "T3", type: "embassy", platform: "X", country: "Germany", region: "Europe", lang: "DE/EN", conf: "H", status: "active", notes: "European hub. Hormuz campaign participant." },
  { id: "@IraninAustria", tier: "T3", type: "embassy", platform: "X", country: "Austria", region: "Europe", lang: "DE/EN", conf: "H", status: "active", notes: "Vienna — UN/IAEA hub. Legal/NPT framing dominant." },
  { id: "@EmbassyofIrtoRF",tier:"T3", type: "embassy", platform: "X", country: "Russia", region: "Europe", lang: "RU/EN", conf: "H", status: "active", notes: "Moscow. 'New Delhi to Moscow' axis. Keys to Hormuz participant." },
  { id: "@IRANinTJ",      tier: "T3", type: "embassy", platform: "X", country: "Tajikistan", region: "Central Asia", lang: "FA/TJ/EN", conf: "H", status: "active", notes: "Tajikistan embassy. Highest single-post: Tajikistan-linked account (Jesus-punches-Trump) — 24.1M views." },
  { id: "@Iran_in_UK",    tier: "T3", type: "embassy", platform: "X", country: "UK", region: "Europe", lang: "EN", conf: "H", status: "active", notes: "'London to Pretoria' axis. Keys to Hormuz participant." },
  { id: "@IRANinMumbai",  tier: "T3", type: "embassy", platform: "X", country: "India", region: "South Asia", lang: "EN/HI", conf: "H", status: "active", notes: "Consulate Mumbai — most substantively documented account. Military updates + meme + diplomatic framing." },
  { id: "@IRANinKENYA",   tier: "T3", type: "embassy", platform: "X", country: "Kenya", region: "Africa", lang: "EN", conf: "H", status: "active", notes: "Africa IW campaign. Prism News documented as part of Africa info-warfare bloc." },
  { id: "@IRANinETHIOPIA",tier: "T3", type: "embassy", platform: "X", country: "Ethiopia", region: "Africa", lang: "EN/AM", conf: "M", status: "active", notes: "Africa bloc campaign." },
  { id: "@IraninAlgeria", tier: "T3", type: "embassy", platform: "X", country: "Algeria", region: "Africa", lang: "FR/AR/EN", conf: "M", status: "active", notes: "Africa/MENA bloc." },
  { id: "@IraninSKorea",  tier: "T3", type: "embassy", platform: "X", country: "South Korea", region: "East Asia", lang: "EN/KO", conf: "M", status: "active", notes: "Asia bloc campaign participant." },
  { id: "@IraninIslamabad",tier:"T3", type: "embassy", platform: "X", country: "Pakistan", region: "South Asia", lang: "EN/UR", conf: "M", status: "active", notes: "Pakistan was ceasefire mediator — politically complex. Solidarity messaging." },
  { id: "@IranInThailand",tier: "T3", type: "embassy", platform: "X", country: "Thailand", region: "SE Asia", lang: "EN/TH", conf: "M", status: "active", notes: "SE Asia bloc." },
  { id: "@IRANinFRANCE",  tier: "T3", type: "embassy", platform: "X", country: "France", region: "Europe", lang: "FR/EN", conf: "M", status: "active", notes: "European bloc. Hormuz messaging." },
  { id: "@IRANinQATAR",   tier: "T3", type: "embassy", platform: "X", country: "Qatar", region: "Middle East", lang: "AR/EN", conf: "M", status: "active", notes: "Qatar as mediator — complex. Ceasefire/solidarity messaging." },
  { id: "@IRANinBRAZIL",  tier: "T3", type: "embassy", platform: "X", country: "Brazil", region: "LatAm", lang: "PT/EN", conf: "M", status: "active", notes: "LatAm bloc." },
  { id: "@IRANINARGENTINA",tier:"T3", type: "embassy", platform: "X", country: "Argentina", region: "LatAm", lang: "ES", conf: "M", status: "active", notes: "LatAm Global South framing." },
  { id: "@Eiranencaracas",tier: "T3", type: "embassy", platform: "X", country: "Venezuela", region: "LatAm", lang: "ES", conf: "L", status: "active", notes: "Venezuela — Iran ally; low confidence." },
  { id: "@iranincuba",    tier: "T3", type: "embassy", platform: "X", country: "Cuba", region: "LatAm", lang: "ES", conf: "L", status: "active", notes: "Cuba — Iran ally." },
  { id: "@IRANinNorway",  tier: "T3", type: "embassy", platform: "X", country: "Norway", region: "Europe", lang: "NO/EN", conf: "L", status: "unknown", notes: "Nordic region." },
  { id: "@IRANinFINLAND", tier: "T3", type: "embassy", platform: "X", country: "Finland", region: "Europe", lang: "FI/EN", conf: "L", status: "unknown", notes: "Nordic region." },
  { id: "@IRANinGREECE",  tier: "T3", type: "embassy", platform: "X", country: "Greece", region: "Europe", lang: "EL/EN", conf: "L", status: "unknown", notes: "SE Europe." },
  { id: "@IRANinHUNGARY", tier: "T3", type: "embassy", platform: "X", country: "Hungary", region: "Europe", lang: "HU/EN", conf: "L", status: "unknown", notes: "Orban-Hungary has closer ties to Iran." },
  { id: "@IRANinROMANIA", tier: "T3", type: "embassy", platform: "X", country: "Romania", region: "Europe", lang: "RO/EN", conf: "L", status: "unknown", notes: "SE Europe." },
  { id: "@IRANinCZECH",   tier: "T3", type: "embassy", platform: "X", country: "Czech Republic", region: "Europe", lang: "CS/EN", conf: "L", status: "unknown", notes: "Central Europe." },
  { id: "@IRANinBELGIQUE",tier: "T3", type: "embassy", platform: "X", country: "Belgium", region: "Europe", lang: "FR/EN", conf: "L", status: "unknown", notes: "Brussels — EU hub adjacent to IranmissionEU." },
  { id: "@IRANinBiH",     tier: "T3", type: "embassy", platform: "X", country: "Bosnia", region: "Europe", lang: "BS/EN", conf: "L", status: "unknown", notes: "Balkan Muslim-majority — target audience." },
  { id: "@IRAN_in_NL",    tier: "T3", type: "embassy", platform: "X", country: "Netherlands", region: "Europe", lang: "NL/EN", conf: "L", status: "unknown", notes: "Netherlands — The Hague (ICJ proximity relevant)." },
  { id: "@IRANinKabul",   tier: "T3", type: "embassy", platform: "X", country: "Afghanistan", region: "Central Asia", lang: "FA/DA", conf: "L", status: "unknown", notes: "Kabul — Taliban government; complex relations." },
  { id: "@IRANINBAKU",    tier: "T3", type: "embassy", platform: "X", country: "Azerbaijan", region: "Caucasus", lang: "AZ/EN", conf: "L", status: "unknown", notes: "Azerbaijan — Iran-Azerbaijani tensions historically high." },
  { id: "@IranAmbIndia",  tier: "T3", type: "embassy", platform: "X", country: "India", region: "South Asia", lang: "EN", conf: "L", status: "active", notes: "Ambassador account (separate from embassy account)." },
  { id: "@IranEmbassyLB", tier: "T3", type: "embassy", platform: "X", country: "Lebanon", region: "Middle East", lang: "AR/EN", conf: "H", status: "active", notes: "Lebanon — Hezbollah territory; strategic." },
  { id: "@IranembassyDam",tier: "T3", type: "embassy", platform: "X", country: "Syria", region: "Middle East", lang: "AR/EN", conf: "L", status: "unknown", notes: "Damascus." },
  { id: "@IraninChina",   tier: "T3", type: "embassy", platform: "X", country: "China", region: "East Asia", lang: "EN/ZH", conf: "M", status: "active", notes: "Beijing — important China-Iran relationship." },
  { id: "@IraninJapan",   tier: "T3", type: "embassy", platform: "X", country: "Japan", region: "East Asia", lang: "EN/JA", conf: "L", status: "unknown", notes: "Tokyo." },
  { id: "@iraninmalaysia",tier: "T3", type: "embassy", platform: "X", country: "Malaysia", region: "SE Asia", lang: "EN/MS", conf: "L", status: "unknown", notes: "KL." },
  { id: "@IraninDhaka",   tier: "T3", type: "embassy", platform: "X", country: "Bangladesh", region: "South Asia", lang: "EN/BN", conf: "L", status: "unknown", notes: "Dhaka." },
  { id: "@IraninIndonesia",tier:"T3", type: "embassy", platform: "X", country: "Indonesia", region: "SE Asia", lang: "EN/ID", conf: "L", status: "unknown", notes: "Jakarta — world's largest Muslim country." },
  { id: "@IraninSerbia",  tier: "T3", type: "embassy", platform: "X", country: "Serbia", region: "Europe", lang: "SR/EN", conf: "L", status: "unknown", notes: "Belgrade." },
  { id: "@IraninSpain",   tier: "T3", type: "embassy", platform: "X", country: "Spain", region: "Europe", lang: "ES/EN", conf: "L", status: "unknown", notes: "Madrid." },
  { id: "@IraninGeorgia", tier: "T3", type: "embassy", platform: "X", country: "Georgia", region: "Caucasus", lang: "EN/KA", conf: "L", status: "unknown", notes: "Tbilisi." },
  { id: "@iraninyerevan", tier: "T3", type: "embassy", platform: "X", country: "Armenia", region: "Caucasus", lang: "EN/HY", conf: "L", status: "unknown", notes: "Yerevan." },
  { id: "@IranNigeria",   tier: "T3", type: "embassy", platform: "X", country: "Nigeria", region: "Africa", lang: "EN", conf: "M", status: "active", notes: "Nigeria — Africa IW bloc." },

  // TIER 4 — State Media
  { id: "@PressTV",       tier: "T4", type: "media", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "H", status: "active", notes: "Flagship English state TV. Blue check removed Feb 2024. Aggressive Telegram/Rumble migration. Hebrew-language Telegram launched Dec 2025." },
  { id: "@IrnaEnglish",   tier: "T4", type: "media", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "H", status: "active", notes: "IRNA wire service. First-mover on official statements." },
  { id: "@EnglishFars",   tier: "T4", type: "media", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "H", status: "active", notes: "Fars News (IRGC-affiliated). Blue check removed Feb 2024. Hormuz corridor videos." },
  { id: "@Tasnimnews_EN", tier: "T4", type: "media", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "H", status: "active", notes: "Tasnim (IRGC-affiliated). Blue check removed Feb 2024. Attacked Araghchi Apr 16 — public coordination failure." },
  { id: "@Tasnimnews_Fa", tier: "T4", type: "media", platform: "X", country: "Iran", region: "Global", lang: "FA", conf: "H", status: "active", notes: "Tasnim Farsi. IRGC diplomatic channel to US during talks." },
  { id: "@Tasnimnews_He", tier: "T4", type: "media", platform: "X", country: "Iran", region: "Global", lang: "HE", conf: "H", status: "active", notes: "Tasnim Hebrew — targets Israeli audiences." },
  { id: "@iribnews_irib", tier: "T4", type: "media", platform: "X", country: "Iran", region: "Global", lang: "FA", conf: "H", status: "active", notes: "IRIB institutional. 9,031 posts. Amplifies PressTV/Tasnim." },
  { id: "@sahartvonline", tier: "T4", type: "media", platform: "X", country: "Iran", region: "South Asia", lang: "UR", conf: "M", status: "active", notes: "Sahar TV Urdu. South Asian audiences. Calibrated given Pakistan's mediator role." },
  { id: "@OfficialSaharTV",tier:"T4", type: "media", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "M", status: "active", notes: "Sahar TV English." },
  { id: "@EnSaharTV",     tier: "T4", type: "media", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "L", status: "unknown", notes: "Sahar TV alternate English handle." },
  { id: "@HispanTV",      tier: "T4", type: "media", platform: "X", country: "Iran", region: "LatAm", lang: "ES", conf: "H", status: "active", notes: "Spanish-language. 44,100 followers Jan 2026. ADL Feb 2026 documented antisemitic content escalation." },
  { id: "@hispantv_brasil",tier:"T4", type: "media", platform: "X", country: "Iran", region: "LatAm", lang: "PT", conf: "M", status: "active", notes: "HispanTV Brazil — Portuguese-language targeting." },
  { id: "@presstvturk",   tier: "T4", type: "media", platform: "X", country: "Iran", region: "Middle East", lang: "TR", conf: "L", status: "unknown", notes: "PressTV Turkish. Low confidence on account status." },
  { id: "@AlalamNews",    tier: "T4", type: "media", platform: "X", country: "Iran", region: "Middle East", lang: "AR", conf: "M", status: "suspended", notes: "Al-Alam TV (IRIB Arabic). Suspended/blocked X, YouTube, Instagram Mar 2024. Now primarily Telegram." },

  // TIER 5 — Individual Influencers
  { id: "@s_m_marandi",   tier: "T5", type: "individual", platform: "X", country: "Iran", region: "Global", lang: "EN", conf: "H", status: "active", notes: "Prof. Seyed Mohammad Marandi. Tehran University. Nuclear negotiations adviser. Most active regime intellectual in English. Frequently cited by Western media." },

  // TIER 6 — Proxy / Resistance Media
  { id: "@AlMayadeenNews",tier: "T6", type: "proxy", platform: "X", country: "Lebanon", region: "Middle East", lang: "AR", conf: "H", status: "active", notes: "Al-Mayadeen. 467K+ posts. Pro-Iran/Hezbollah. Briefly suspended Jan 2024. Arabic-sphere coordinator." },
  { id: "@MayadeenEnglish",tier:"T6", type: "proxy", platform: "X", country: "Lebanon", region: "Middle East", lang: "EN", conf: "H", status: "active", notes: "Al-Mayadeen English. Temporarily suspended 12h Jan 2024." },
  { id: "@AlMayadeenNews", tier: "T6", type: "proxy", platform: "X", country: "Lebanon", region: "Middle East", lang: "AR", conf: "H", status: "active", notes: "Al-Mayadeen main Arabic account." },
];

// ── VERIFIED POSTS WITH ENGAGEMENT DATA ───────────────────────────────────────
const VIRAL_POSTS = [
  { rank: 1, account: "@IraninZimbabwe", date: "2026-04-05", text: "We've lost the keys.", views: 6900000, likes: 93000, campaign: "keys_to_hormuz", x_url: "https://x.com/IRANinZIMBABWE/status/2041666510238650422" },
  { rank: 2, account: "@IraninSA",       date: "2026-04-13", text: "AI meme: Trump/Vance/Hegseth as 'miserable pirates of the Persian Gulf'", views: 3100000, likes: null, campaign: "pirates_of_hormuz" },
  { rank: 3, account: "@IraninZimbabwe", date: "2026-04-07", text: "We found the keys.", views: 1900000, likes: null, campaign: "keys_to_hormuz", x_url: "https://x.com/IRANinZIMBABWE/status/2041666510238650422" },
  { rank: 4, account: "@IraninSA",       date: "2026-04-05", text: "Toy steering wheel meme — mocking Trump's Hormuz control claim", views: 3100000, likes: null, campaign: "keys_to_hormuz" },
  { rank: 5, account: "@IRANinTJ linked",date: "2026-04-xx", text: "Jesus-punches-Trump meme (Tajikistan-linked account, Explosive Media)", views: 24100000, likes: null, campaign: "af_iw", notes: "Via Explosive Media / Revayat-e Fath — semi-independent but IRI-adjacent" }
];

// ── AGGREGATE METRICS (ISD Global, Apr 24 2026) ───────────────────────────────
const AGGREGATE_METRICS = {
  period: "First 50 days of war (Feb 28 – Apr 18 approx.)",
  total_views: "~900 million",
  total_likes: "~22 million",
  likes_increase_vs_prior: "30x",
  shares: "76 million (prev: 4.3M)",
  comments: "870,000 (prev: 191,000)",
  source: "ISD Global / Al Jazeera / Soufan Center Apr 24 2026"
};

// ── ANALYSIS IDEAS (12 visualizations) ───────────────────────────────────────
const ANALYSIS_IDEAS = [
  { id: 1, title: "Trump Trigger → Response Time", question: "How fast does the network respond to Trump posts, by tier?", chart: "Violin plot per tier, x=hours after Trump post", data_fields: ["trump_post_timestamp", "embassy_post_timestamp", "tier", "narrative"] },
  { id: 2, title: "Narrative Flow Sankey", question: "Who seeds a narrative and in what order does it spread?", chart: "Sankey diagram — nodes=accounts, edges=narrative transmission by time", data_fields: ["post_timestamps", "narrative_type", "tier", "coordinated_flag"] },
  { id: 3, title: "Narrative Drift Timeline", question: "How did dominant frame shift across conflict phases?", chart: "Stacked area chart with event markers + small multiples by tier", data_fields: ["date", "narrative_type", "conflict_phase", "tone_formal_vs_meme"] },
  { id: 4, title: "Language Targeting Map", question: "Are accounts targeting by geography or ideology?", chart: "Chord diagram: language vs. target region", data_fields: ["post_lang", "account_location", "tier", "follower_geography"] },
  { id: 5, title: "Coordination Heatmap", question: "Which accounts coordinate most tightly?", chart: "Heatmap: accounts × accounts, cell = same-day same-narrative days. Hierarchical clustering.", data_fields: ["post_date", "narrative_type", "account", "tier"] },
  { id: 6, title: "Escalation Ladder", question: "Does Iran's narrative aggression mirror Trump or have its own rhythm?", chart: "Dual-axis line: Trump aggression (3-day rolling avg) vs. Iranian response aggression", data_fields: ["trump_aggression", "embassy_tone", "conflict_phase", "event_dates"] },
  { id: 7, title: "Behavioral PCA Clustering", question: "Do accounts actually cluster as T1-T6 predicts?", chart: "UMAP scatter — each dot = account, color = tier, shape = language group", data_fields: ["posts_per_day", "response_lag", "narrative_distribution", "coordination_score", "tone_score"] },
  { id: 8, title: "First-Mover Detection", question: "Which account seeds each campaign and which just amplify?", chart: "Per-campaign: horizontal timeline showing posting sequence by tier", data_fields: ["post_timestamps", "campaign_flag", "tier", "engagement"] },
  { id: 9, title: "Platform Fragmentation Map", question: "When X restricts, where does content migrate?", chart: "Parallel coordinates: X / Telegram / Rumble / YouTube / Website per account", data_fields: ["platform_presence", "suspension_status", "follower_count_per_platform"] },
  { id: 10, title: "Inauthentic Amplification Overlay", question: "What % of virality came from BRICS4CLICKS / Verified4War?", chart: "Stacked bar: top 20 viral posts, segments = organic / ISD network / Russian diplomat", data_fields: ["viral_post_id", "total_engagement", "inauthentic_flag", "network_source"] },
  { id: 11, title: "Geographic Silence Map", question: "Which embassies are conspicuously absent and why?", chart: "Choropleth world map — embassy post volume, silence = distinct color", data_fields: ["embassy_country", "post_volume", "diplomatic_status", "baseline_vs_war_period"] },
  { id: 12, title: "Data Confidence Decay", question: "Which parts of the dataset are reliable vs. directional?", chart: "Line chart: proportion H/M/L confidence data points over time", data_fields: ["confidence_level", "date_sourced", "verification_method"] }
];

// ── EXPORTS ───────────────────────────────────────────────────────────────────
// For use in HTML files: <script src="data.js"></script>
// Then access: TRUMP_POSTS, KEY_EVENTS, CAMPAIGNS, ACCOUNTS, VIRAL_POSTS, etc.
