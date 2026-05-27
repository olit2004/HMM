const tagMap = {
    // Nouns
    'nn': { full: 'Noun, singular or mass', category: 'pos-noun' },
    'nns': { full: 'Noun, plural', category: 'pos-noun' },
    'np': { full: 'Proper noun, singular', category: 'pos-noun' },
    'nps': { full: 'Proper noun, plural', category: 'pos-noun' },
    'nr': { full: 'Adverbial noun', category: 'pos-noun' },
    'nrs': { full: 'Plural adverbial noun', category: 'pos-noun' },
    
    // Verbs
    'vb': { full: 'Verb, base form', category: 'pos-verb' },
    'vbd': { full: 'Verb, past tense', category: 'pos-verb' },
    'vbg': { full: 'Verb, gerund/present participle', category: 'pos-verb' },
    'vbn': { full: 'Verb, past participle', category: 'pos-verb' },
    'vbp': { full: 'Verb, non-3rd person singular present', category: 'pos-verb' },
    'vbz': { full: 'Verb, 3rd person singular present', category: 'pos-verb' },
    'md': { full: 'Modal verb', category: 'pos-verb' },
    'be': { full: 'Verb "be", infinitive', category: 'pos-verb' },
    'bez': { full: 'Verb "be", 3rd person singular present', category: 'pos-verb' },
    'bedz': { full: 'Verb "be", past tense', category: 'pos-verb' },
    'ben': { full: 'Verb "be", past participle', category: 'pos-verb' },
    'do': { full: 'Verb "do", base form', category: 'pos-verb' },
    'dod': { full: 'Verb "do", past tense', category: 'pos-verb' },
    'doz': { full: 'Verb "do", 3rd person singular present', category: 'pos-verb' },
    'hv': { full: 'Verb "have", base form', category: 'pos-verb' },
    'hvd': { full: 'Verb "have", past tense', category: 'pos-verb' },
    'hvz': { full: 'Verb "have", 3rd person singular present', category: 'pos-verb' },
    
    // Adjectives
    'jj': { full: 'Adjective', category: 'pos-adj' },
    'jjr': { full: 'Adjective, comparative', category: 'pos-adj' },
    'jjs': { full: 'Adjective, superlative', category: 'pos-adj' },
    
    // Adverbs
    'rb': { full: 'Adverb', category: 'pos-adv' },
    'rbr': { full: 'Adverb, comparative', category: 'pos-adv' },
    'rbs': { full: 'Adverb, superlative', category: 'pos-adv' },
    'wrb': { full: 'Wh-adverb', category: 'pos-adv' },
    'rn': { full: 'Nominal adverb', category: 'pos-adv' },
    'ql': { full: 'Qualifier', category: 'pos-adv' },
    'ap': { full: 'Post-determiner', category: 'pos-adv' },
    
    // Pronouns
    'pps': { full: 'Personal pronoun, subject', category: 'pos-pron' },
    'ppo': { full: 'Personal pronoun, object', category: 'pos-pron' },
    'pp$': { full: 'Possessive pronoun', category: 'pos-pron' },
    'ppss': { full: 'Personal pronoun, plural', category: 'pos-pron' },
    'pn': { full: 'Nominal pronoun', category: 'pos-pron' },
    'wp': { full: 'Wh-pronoun', category: 'pos-pron' },
    'wps': { full: 'Wh-pronoun, nominative', category: 'pos-pron' },
    'wp$': { full: 'Possessive wh-pronoun', category: 'pos-pron' },
    'ppl': { full: 'Singular reflexive/intensive pronoun', category: 'pos-pron' },
    'ppls': { full: 'Plural reflexive/intensive pronoun', category: 'pos-pron' },
    
    // Prepositions and Conjunctions
    'in': { full: 'Preposition', category: 'pos-prep' },
    'cc': { full: 'Coordinating conjunction', category: 'pos-conj' },
    'cs': { full: 'Subordinating conjunction', category: 'pos-conj' },
    
    // Determiners and Articles
    'dt': { full: 'Determiner', category: 'pos-det' },
    'dts': { full: 'Plural determiner', category: 'pos-det' },
    'dtx': { full: 'Determiner/double conjunction', category: 'pos-det' },
    'at': { full: 'Article', category: 'pos-det' },
    'wdt': { full: 'Wh-determiner', category: 'pos-det' },
    'abn': { full: 'Pre-quantifier', category: 'pos-det' },
    
    // Others
    'cd': { full: 'Cardinal number', category: 'pos-other' },
    'od': { full: 'Ordinal number', category: 'pos-other' },
    'ex': { full: 'Existential there', category: 'pos-other' },
    'fw': { full: 'Foreign word', category: 'pos-other' },
    'rp': { full: 'Particle', category: 'pos-prep' },
    'to': { full: 'Infinitive marker "to"', category: 'pos-prep' },
    'uh': { full: 'Interjection', category: 'pos-other' },
    '*': { full: 'Negator (not)', category: 'pos-other' },
    '.': { full: 'Punctuation, sentence closer', category: 'pos-other' },
    ',': { full: 'Punctuation, comma', category: 'pos-other' },
    ':': { full: 'Punctuation, colon/semicolon', category: 'pos-other' },
    '(': { full: 'Left parenthesis', category: 'pos-other' },
    ')': { full: 'Right parenthesis', category: 'pos-other' },
    '``': { full: 'Opening quotation mark', category: 'pos-other' },
    "''": { full: 'Closing quotation mark', category: 'pos-other' },
    "--": { full: 'Dash', category: 'pos-other' }
};

function getTagInfo(rawAbbr) {
    // lowercase the tag from backend
    let abbr = rawAbbr.toLowerCase();
    
    // Strip common Brown corpus suffixes like -tl (title), -hl (headline), -nc (not cited)
    abbr = abbr.split('-')[0];
    
    // Strip compound tag markers (e.g. fw-nn) by just taking the base if foreign word
    if (abbr.startsWith('fw') && abbr !== 'fw') {
        abbr = abbr.replace('fw-', ''); // just use the base word class
    }
    
    // Check exact match
    if (tagMap[abbr]) {
        return tagMap[abbr];
    }
    
    // Check if it's a known punctuation 
    if (['.', ',', ':', ';', '!', '?', '(', ')', '"', "'", '`', '-'].includes(abbr[0])) {
         return { full: 'Punctuation', category: 'pos-other' };
    }
    
    // Prefix fallback mapping
    const fallbackPrefixes = {
        'nn': { full: 'Noun (derived)', category: 'pos-noun' },
        'vb': { full: 'Verb (derived)', category: 'pos-verb' },
        'jj': { full: 'Adjective (derived)', category: 'pos-adj' },
        'rb': { full: 'Adverb (derived)', category: 'pos-adv' },
        'pp': { full: 'Pronoun (derived)', category: 'pos-pron' },
        'dt': { full: 'Determiner (derived)', category: 'pos-det' },
        'at': { full: 'Article (derived)', category: 'pos-det' },
        'in': { full: 'Preposition (derived)', category: 'pos-prep' },
        'cc': { full: 'Conjunction (derived)', category: 'pos-conj' },
        'cs': { full: 'Conjunction (derived)', category: 'pos-conj' },
    };
    
    for (const [prefix, val] of Object.entries(fallbackPrefixes)) {
        if (abbr.startsWith(prefix)) {
            return val;
        }
    }
    
    return { full: 'Unknown/Other', category: 'pos-other' };
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('tagForm');
    const input = document.getElementById('sentenceInput');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.querySelector('.btn-text');
    const clearBtn = document.getElementById('clearBtn');
    const resultsSection = document.getElementById('resultsSection');
    const tagsContainer = document.getElementById('tagsContainer');
    const errorMessage = document.getElementById('errorMessage');

    if(clearBtn) {
        clearBtn.addEventListener('click', () => {
            input.value = '';
            resultsSection.classList.add('hidden');
            tagsContainer.innerHTML = '';
            errorMessage.classList.add('hidden');
            input.focus();
        });
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const sentence = input.value.trim();
        if (!sentence) return;

        // UI Loading State
        submitBtn.disabled = true;
        btnText.textContent = 'Tagging...';
        errorMessage.classList.add('hidden');
        resultsSection.classList.add('hidden');
        tagsContainer.innerHTML = '';

        try {
            const response = await fetch('/api/tag', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ sentence })
            });

            if (!response.ok) {
                let errorData;
                try {
                    errorData = await response.json();
                } catch(e) {
                    throw new Error(`Server returned ${response.status}`);
                }
                throw new Error(errorData.detail || 'Failed to tag sentence');
            }

            const data = await response.json();
            
            // Render results
            data.forEach((item, index) => {
                const info = getTagInfo(item.tag);
                
                const card = document.createElement('div');
                card.className = `tag-card ${info.category}`;
                card.style.animationDelay = `${index * 0.03}s`;
                
                card.innerHTML = `
                    <span class="word">${escapeHTML(item.word)}</span>
                    <div class="pos-badge">
                        <span class="pos-abbr">${escapeHTML(item.tag.toUpperCase())}</span>
                        <span class="pos-full">${escapeHTML(info.full)}</span>
                    </div>
                `;
                
                tagsContainer.appendChild(card);
            });
            
            resultsSection.classList.remove('hidden');
            
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('hidden');
        } finally {
            // Reset UI State
            submitBtn.disabled = false;
            btnText.textContent = 'Tag Sentence';
        }
    });

    function escapeHTML(str) {
        const p = document.createElement('p');
        p.appendChild(document.createTextNode(str));
        return p.innerHTML;
    }
});
