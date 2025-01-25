# Instruction Following Evaluators Documentation


## 1. Keyword Existence
- **Instruction ID**: `keywords:existence`
- **Class**: `KeywordChecker`
- **Description**: Checks if specific keywords appear in the response
- **Parameters**:
  - `keywords`: List[str] - List of keywords to check for

## 2. Keyword Frequency
- **Instruction ID**: `keywords:frequency`
- **Class**: `KeywordFrequencyChecker` 
- **Description**: Checks how many times a specific keyword appears
- **Parameters**:
  - `keyword`: str - The keyword to count
  - `frequency`: int - Target frequency
  - `relation`: str - Either "at least" or "less than"

## 3. Forbidden Words
- **Instruction ID**: `keywords:forbidden_words`
- **Class**: `ForbiddenWords`
- **Description**: Ensures specific words do not appear in the response
- **Parameters**:
  - `forbidden_words`: List[str] - Words that should not appear

## 4. Letter Frequency
- **Instruction ID**: `keywords:letter_frequency`
- **Class**: `LetterFrequencyChecker`
- **Description**: Counts occurrences of a specific letter
- **Parameters**:
  - `letter`: str - The letter to count
  - `let_frequency`: int - Target frequency
  - `let_relation`: str - Either "at least" or "less than"

## 5. Response Language
- **Instruction ID**: `language:response_language`
- **Class**: `ResponseLanguageChecker`
- **Description**: Verifies the language of the response
- **Parameters**:
  - `language`: str - ISO 639-1 language code (e.g., 'en', 'es')

## 6. Number of Sentences
- **Instruction ID**: `length_constraints:number_sentences`
- **Class**: `NumberOfSentences`
- **Description**: Checks the number of sentences in the response
- **Parameters**:
  - `num_sentences`: int - Target number of sentences
  - `relation`: str - Either "at least" or "less than"

## 7. Paragraph Count
- **Instruction ID**: `length_constraints:number_paragraphs`
- **Class**: `ParagraphChecker`
- **Description**: Verifies the number of paragraphs (separated by ***)
- **Parameters**:
  - `num_paragraphs`: int - Required number of paragraphs

## 8. Word Count
- **Instruction ID**: `length_constraints:number_words`
- **Class**: `NumberOfWords`
- **Description**: Counts the total number of words
- **Parameters**:
  - `num_words`: int - Target word count
  - `relation`: str - Either "at least" or "less than"

## 9. Paragraph First Word
- **Instruction ID**: `length_constraints:nth_paragraph_first_word`
- **Class**: `ParagraphFirstWordCheck`
- **Description**: Checks first word of specified paragraph
- **Parameters**:
  - `paragraph_index`: int - Which paragraph to check
  - `first_word`: str - Expected first word

## 10. Placeholder Count
- **Instruction ID**: `detectable_content:number_placeholders`
- **Class**: `PlaceholderChecker`
- **Description**: Counts placeholders marked with [brackets]
- **Parameters**:
  - `num_placeholders`: int - Minimum number of placeholders required

## 11. Postscript Check
- **Instruction ID**: `detectable_content:postscript`
- **Class**: `PostscriptChecker`
- **Description**: Verifies presence of P.S. or P.P.S.
- **Parameters**:
  - `postscript_marker`: str - Either "P.S." or "P.P.S"

## 12. Bullet List Count
- **Instruction ID**: `detectable_format:number_bullet_lists`
- **Class**: `BulletListChecker`
- **Description**: Counts bullet points (starting with *)
- **Parameters**:
  - `num_bullet_lists`: int - Required number of bullet points

## 13. Constrained Response
- **Instruction ID**: `detectable_format:constrained_response`
- **Class**: `ConstrainedResponseChecker`
- **Description**: Checks if response matches predefined options
- **Parameters**: None (uses predefined options)

## 14. Highlighted Sections
- **Instruction ID**: `detectable_format:number_highlighted_sections`
- **Class**: `HighlightSectionChecker`
- **Description**: Counts highlighted sections
- **Parameters**:
  - `num_highlights`: int - Required number of highlights

## 15. Multiple Sections
- **Instruction ID**: `detectable_format:multiple_sections`
- **Class**: `SectionChecker`
- **Description**: Verifies section structure and count
- **Parameters**:
  - `section_spliter`: str - Either "Section" or "SECTION"
  - `num_sections`: int - Required number of sections

## 16. JSON Format
- **Instruction ID**: `detectable_format:json_format`
- **Class**: `JsonFormat`
- **Description**: Validates JSON formatting
- **Parameters**: None

## 17. Title Check
- **Instruction ID**: `detectable_format:title`
- **Class**: `TitleChecker`
- **Description**: Checks for title in <<brackets>>
- **Parameters**: None

## 18. Two Responses
- **Instruction ID**: `combination:two_responses`
- **Class**: `TwoResponsesChecker`
- **Description**: Verifies two distinct responses are provided
- **Parameters**: None

## 19. Repeat Prompt
- **Instruction ID**: `combination:repeat_prompt`
- **Class**: `RepeatPromptThenAnswer`
- **Description**: Checks if prompt is repeated before answer
- **Parameters**:
  - `prompt`: str - Original prompt to check for

## 20. End Checker
- **Instruction ID**: `startend:end_checker`
- **Class**: `EndChecker`
- **Description**: Verifies response ends with specific phrase
- **Parameters**:
  - `ending`: str - Required ending phrase

## 21. Capital Word Frequency
- **Instruction ID**: `change_case:capital_word_frequency`
- **Class**: `CapitalWordFrequencyChecker`
- **Description**: Counts words in ALL CAPS
- **Parameters**:
  - `capital_frequency`: int - Target frequency
  - `capital_relation`: str - Either "at least" or "less than"

## 22. English Capitals
- **Instruction ID**: `change_case:english_capital`
- **Class**: `CapitalLettersEnglishChecker`
- **Description**: Checks if response is in English and ALL CAPS
- **Parameters**: None

## 23. English Lowercase
- **Instruction ID**: `change_case:english_lowercase`
- **Class**: `LowercaseLettersEnglishChecker`
- **Description**: Checks if response is in English and lowercase
- **Parameters**: None

## 24. No Comma
- **Instruction ID**: `punctuation:no_comma`
- **Class**: `CommaChecker`
- **Description**: Verifies absence of commas
- **Parameters**: None

## 25. Quotation Check
- **Instruction ID**: `startend:quotation`
- **Class**: `QuotationChecker`
- **Description**: Checks if response is wrapped in quotation marks
- **Parameters**: None