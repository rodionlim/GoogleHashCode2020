pizzaProb:{[filehandler;combi]
    / Usage: pizzaProb[`:a_example.in;0] | pizzaProb[`:b_small.in;0] | pizzaProb[`:c_medium.in;0] | pizzaProb[`:d_quite_big.in;7] | pizzaProb[`:e_also_big.in;0]

    / Input Parsing and Internal Definitions
    {{`c set x . 0 0;`input set x 1;`rv set reverse}("J"$" "vs/:x)}read0 filehandler;
    t:rv ([]idx:til count input;slices:input); / Sort in descending slices size
    
    / Main Computation Algorithm
    res:{
            {x first where x[`slices]=max x`slices}
            raze {
                t:y _ x; / For each iteration, we drop the biggest slice from the list
                t:enlist[t],{[t;p].[{x _ y};(t;p);0#t]}[t;] each 1+til z; / Skip 1 or more to cater for cases like "3 3 3 8 90" | constraint 100
                {exec idx,sum slices from (update csum:({$[c>=x+y;x+y;x]}\) slices from x) where not csum=prev csum} each t / Greedy algorithm, select slices till constraint met
                }[x;;y] each where c<=rv sums rv x`slices / Optimization to stop iteration once sum of all slices more than constraint
            }[t;combi];

    / Output parsing
    (`$ssr[string filehandler; ".in";".out"]) 0: {" "sv/: string (enlist count x;x)} rv res`idx
    };