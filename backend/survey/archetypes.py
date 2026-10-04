"""Spiritual gift archetypes and matching logic.

An archetype is a gift signature (a blend of spiritual gifts), not a single gift.
Each archetype maps to the ministry family and roles it fits in a faith-based
institution. Matching uses a participant's ranked gift scores against each
archetype's signature.
"""

ARCHETYPES = [
    {
        'name': 'The Pioneer',
        'family': 'Reach',
        'tagline': 'Starts what doesn\'t yet exist.',
        'description': 'Sees the unreached frontier, trusts God for provision, and gathers others to launch new work.',
        'signature': ['Apostleship', 'Faith', 'Leadership', 'Wisdom'],
        'roles': ['Church planting', 'Mission director', 'Conference/senior leadership', 'Vision-casting'],
        'engage': 'Give them a frontier, not a system to maintain.',
    },
    {
        'name': 'The Herald',
        'family': 'Reach',
        'tagline': 'Wins hearts for the Kingdom.',
        'description': 'Communicates the gospel with clarity and urgency, and calls others to respond.',
        'signature': ['Evangelism', 'Faith', 'Exhortation'],
        'roles': ['Public evangelism', 'Community outreach', 'Revival meetings', 'Street/market ministry', 'Personal witnessing'],
        'engage': 'Put them in front of the unchurched, not in committee rooms.',
    },
    {
        'name': 'The Prophet',
        'family': 'Reach',
        'tagline': 'Speaks truth the church needs to hear.',
        'description': 'Proclaims God\'s Word boldly and distinguishes truth from error on behalf of the body.',
        'signature': ['Prophecy', 'Discernment', 'Knowledge'],
        'roles': ['Preaching rotation', 'Spiritual accountability', 'Doctrinal watch', 'Calling the church to faithfulness'],
        'engage': 'Pair them with mercy gifts so truth lands with love.',
    },
    {
        'name': 'The Sage',
        'family': 'Reach',
        'tagline': 'Makes truth stick and apply.',
        'description': 'Gathers, clarifies, and communicates truth in a way that transforms how people live.',
        'signature': ['Teaching', 'Knowledge', 'Wisdom'],
        'roles': ['Sabbath School', 'Bible study', 'Equipping/training', 'Curriculum', 'Mentoring future teachers'],
        'engage': 'Hand them a classroom and a student, not a spreadsheet.',
    },
    {
        'name': 'The Shepherd',
        'family': 'Keep',
        'tagline': 'Tends the flock one soul at a time.',
        'description': 'Nurtures, cares for, and guides individuals toward spiritual maturity.',
        'signature': ['Shepherding', 'Mercy', 'Exhortation'],
        'roles': ['Pastoral care', 'Small-group leader', 'Visitation', 'Counseling', 'Discipleship'],
        'engage': 'Give them a few people to love deeply, not a crowd to manage.',
    },
    {
        'name': 'The Encourager',
        'family': 'Keep',
        'tagline': 'Meets people in the valley and walks them up.',
        'description': 'Comes alongside the struggling, wounded, and drifting to comfort and re-engage them.',
        'signature': ['Exhortation', 'Mercy', 'Shepherding'],
        'roles': ['New-member assimilation', 'Follow-up', 'One-on-one mentoring', 'Hospital visits', 'Recovery groups'],
        'engage': 'Point them at the ones drifting — they will re-engage them.',
    },
    {
        'name': 'The Watchman',
        'family': 'Keep',
        'tagline': 'Protects the church\'s truth and health.',
        'description': 'Senses what is off, harmful, or counterfeit and protects the body with wisdom.',
        'signature': ['Discernment', 'Knowledge', 'Wisdom'],
        'roles': ['Elder board', 'Doctrinal review', 'Prayer ministry', 'Spiritual warfare', 'Gatekeeping'],
        'engage': 'Let them guard the door; thank them for what they prevent.',
    },
    {
        'name': 'The Comforter',
        'family': 'Keep',
        'tagline': 'Prays heaven into earth\'s hardest rooms.',
        'description': 'Carries the burdens of others to God with confidence and compassionate presence.',
        'signature': ['Faith', 'Discernment', 'Mercy'],
        'roles': ['Intercessory prayer', 'Crisis care', 'Grief ministry', 'Praying over decisions'],
        'engage': 'Give them a prayer list and the hurting; shield their quiet time.',
    },
    {
        'name': 'The Organizer',
        'family': 'Build',
        'tagline': 'Turns vision into a running system.',
        'description': 'Orders ideas, resources, time, and people so ministry actually happens.',
        'signature': ['Administration', 'Leadership', 'Service/Helps'],
        'roles': ['Church clerk', 'Board member', 'Event logistics', 'Department coordination', 'Records'],
        'engage': 'Let them run operations; don\'t make them the public face.',
    },
    {
        'name': 'The Servant',
        'family': 'Build',
        'tagline': 'Holds up the tent in the background.',
        'description': 'Meets practical unmet needs with quiet, cheerful, behind-the-scenes faithfulness.',
        'signature': ['Service/Helps', 'Mercy', 'Hospitality'],
        'roles': ['Deacons', 'Facilities/maintenance', 'Community services', 'Feeding ministries', 'Setup/cleanup'],
        'engage': 'Give them concrete tasks and genuine thanks; never let them become invisible.',
    },
    {
        'name': 'The Steward',
        'family': 'Build',
        'tagline': 'Fuels the mission with resources.',
        'description': 'Mobilizes material resources generously and wisely to advance God\'s work.',
        'signature': ['Giving', 'Administration', 'Service/Helps'],
        'roles': ['Stewardship dept', 'Trust/benevolence fund', 'Generosity campaigns', 'Missions funding'],
        'engage': 'Give them numbers and a cause; trust their discretion.',
    },
    {
        'name': 'The Host',
        'family': 'Build',
        'tagline': 'Makes strangers feel at home.',
        'description': 'Opens doors, sets tables, and makes every visitor feel valued and welcomed.',
        'signature': ['Hospitality', 'Mercy', 'Service/Helps'],
        'roles': ['Greeter team', 'Fellowship/potluck', 'Visitor welcome', 'Assimilation events', 'Guest lodging'],
        'engage': 'Put them at every doorway and every table.',
    },
]

# Number of a participant's top-ranked gifts used for matching.
MATCH_WINDOW = 5


def match_archetypes(gift_scores):
    """Return ranked archetype matches for a dict of gift_name -> score.

    Each result contains the archetype, a raw score, and a match percentage
    (score / max possible for that archetype). Sorted best-first.
    """
    ranked = [name for name, _ in sorted(
        gift_scores.items(), key=lambda item: item[1], reverse=True
    )]
    top = set(ranked[:MATCH_WINDOW])

    matches = []
    for archetype in ARCHETYPES:
        signature = archetype['signature']
        max_possible = sum(len(signature) - i for i in range(len(signature)))
        score = 0
        for i, gift in enumerate(signature):
            weight = len(signature) - i  # primary gift weighted highest
            if gift in top:
                score += weight

        percentage = round((score / max_possible) * 100, 1) if max_possible else 0.0
        matches.append((archetype, score, percentage))

    matches.sort(key=lambda item: item[1], reverse=True)
    return matches


def archetype_summary(archetype, percentage, is_primary):
    """Shape an archetype for API responses."""
    return {
        'name': archetype['name'],
        'family': archetype['family'],
        'tagline': archetype['tagline'],
        'description': archetype['description'],
        'signature': archetype['signature'],
        'roles': archetype['roles'],
        'engage': archetype['engage'],
        'match_percentage': percentage,
        'is_primary': is_primary,
    }