# Subset construction algorithm:
################################
# function DFA(K, Z, D, s, F) 
#   K' <- list that contains only E-closure(s), unmarked 
#   while there is an unmarked state T in K' do
#     mark T
#     for each symbol a E Z do
#       U <- E-closure(move(T, a)) 
#       if U E/ K' then
#         add U as an unmarked state to K'
#       d[T, a] <- U
#     end 
#   end
#   return <the corresponding DFA> 
# end
################################

# kappa = finite set of states
# sigma = input alphabet
# delta = transition function
# esh = element kappa is the start state
# digamma = subsumes kappa is the set of final accepting states

# Not really sure what format kappa will be in
def sca(kappa, sigma, delpha, esh, digamma):
    # Mark kappa for unmarkedness. 
    # This should get only set of NFA states reachable from state s using E
    # transitions
    for x in range(len(kappa)): kappa[x] = [kappa[x],0]
    # While there are more states to try:
    while kappa[x][1] == 0:
        #Mark T
        kappa[x][1] = 1
        # For each symbol in the input alphabet
        for symbol in sigma:
            # return the amount set of NFA states reachable from that symbol
            # using kappa



if __name__ == '__main__':
    sca(['abba', 'prince'], 0,0,0,0)

