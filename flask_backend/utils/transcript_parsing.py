def process_transcript(transcript, max_words = 300, buffer = 2):
    """
    Splits a transcript into chunks of approximately `max_words` words per part. If `buffer` 
    is greater than 0, each part is buffered by `buffer` lines from the preceding and following parts 
    (if available).

    Args:
        transcript (str): The transcript to process.
        max_words (int): The maximum number of words per part (default 250).
        buffer (int): The number of lines to buffer each part by (default 2).

    Returns:
        A list of lists, where each inner list contains the lines of one part of the transcript. 
        If `buffer` is greater than 0, each part will be buffered by `buffer` lines 
        from the preceding and following parts (if available).
    """
    lines = transcript.split('\n')

    cur_word_count = 0
    all_parts = []
    part = []
    for line in lines:
        if not line:
            continue
        else:
            line_length = len(line.split())

            # Add line to current part if it's under the max word count
            if cur_word_count + line_length <= max_words:
                part.append(line)
                cur_word_count += line_length

            # start a new part if exceed max word
            if cur_word_count + line_length > max_words:
                all_parts.append(part)
                cur_word_count = 0
                part = []
    
    # make sure we do not miss last part
    if part != []:
        all_parts.append(part)

    if buffer == 0:
        return all_parts
    
    buffered_all_parts = []

    if len(all_parts) >= 2:

        for i in range(len(all_parts)):

            cur_part = all_parts[i].copy()

            # head, only add 2 from the next one, if we have the next one

            if i == 0:

                # the min() make sure that we have buffer <= number of lines in previous part
                for j in range(min(buffer, len(all_parts[i + 1]))):
                    cur_part.append(all_parts[i + 1][j])

            # tail, only add 2 from the previous one, if we have previous one

            elif i == len(all_parts) - 1:
                for j in range(min(buffer, len(all_parts[i - 1]))):
                    cur_part.insert(0, all_parts[i - 1][-j - 1])

            else:
                # grab lines from both previous and next one

                for j in range(min(buffer, len(all_parts[i + 1]))):
                    cur_part.append(all_parts[i + 1][j])

                for j in range(min(buffer, len(all_parts[i - 1]))):
                    cur_part.insert(0, all_parts[i - 1][-j - 1])
            
            buffered_all_parts.append(cur_part)

    return buffered_all_parts