def carnatic_notes_to_frequencies(base_frequency, num_octaves=1):
    ratios = {
        'S': 16/15,
        'R': 9/8,
        'G': 5/4,
        'M': 4/3,
        'P': 3/2,
        'D': 5/3,
        'N': 15/8
    }
    note_frequencies = {}
    for note, ratio in ratios.items():
        note_frequencies[note] = [base_frequency * (ratio ** (octave + 1)) for octave in range(num_octaves)]
    return note_frequencies
