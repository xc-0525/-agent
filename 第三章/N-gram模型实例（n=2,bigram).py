import collections

# 示例语料库，与上方案例讲解中的语料库保持一致
corpus = "datawhale agent learns datawhale agent works"
tokens = corpus.split()
total_tokens = len(tokens)

count_agent = tokens.count('agent')
p_agent = count_agent / total_tokens
print(f"第一步: P(agent) = {count_agent}/{total_tokens} = {p_agent:.3f}")

bigrams = zip(tokens, tokens[1:])
bigram_counts = collections.Counter(bigrams)
count_agent_works = bigram_counts[('agent', 'works')]

p_agent_given_works = count_agent_works / count_agent
print(f"第二步: P(agent|works) = {count_agent_works}/{count_agent} = {p_agent_given_works:.3f}")


p_sentence = p_agent * p_agent_given_works
print(f"最后: P('agent works') ≈ {p_agent:.3f} * {p_agent_given_works:.3f} = {p_sentence:.3f}")

#>>>
#第一步: P(datawhale) = 2/6 = 0.333
#第二步: P(agent|datawhale) = 2/2 = 1.000
#第三步: P(learns|agent) = 1/2 = 0.500
#最后: P('datawhale agent learns') ≈ 0.333 * 1.000 * 0.500 = 0.167
