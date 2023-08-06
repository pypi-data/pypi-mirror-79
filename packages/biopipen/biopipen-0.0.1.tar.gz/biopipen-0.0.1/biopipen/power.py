"""Power analysis"""
from diot import Diot
from . import opts, proc_factory

# pylint: disable=invalid-name

pSurvivalPower = proc_factory(
    desc="Survival analysis.",
    config=Diot(annotate="""
    @name:
        pSurvivalPower
    @description:
        Do power analysis for survival analysis.
        See http://www.sample-size.net/sample-size-survival-analysis/
    @input:
        `infile:file`: The input file, could be either:
            - detailed suvival data with [`patient`, ]`time`, `status`, `variable1`, `variable2`, ...; or
            - ratios with `variable`, `survrate1`, `survrate2`, `ssratio`, where `survrate1` and
                `survrate2` are survival rates in group1 and group2, respectively,
                and `ssratio` is sample size ratio in group1/group2
        `ngroup1`: The size of 1st group, for detailed input file
        `ngroup2`: The size of 2nd group, for detailed input file
        `ngroup3`: The size of 3rd group, for detailed input file
        `ngroup4`: The size of 4th group, for detailed input file
    @output:
        `outfile:file`: The output file with columns:
            - Variable: the variable (including paired groups)
            - Alpha: the alpha value
            - Beta: the beta value (1-power)
            - SSize1: the sample size for group1
            - SSize2: the sample size for group2
            - Total: the total sample size
    @args:
        `rnames`: Whether the detailed input file has row names. Default: `True`
        `plot`  : Plot the results? Default: `False`
        `ngroup`: Number of groups to divide into for detailed input file. Default: `2`
        `intype`: The input file type. Either `detailed` (default) or `ratio`
        `alphas`: The alpha values (two-sided). You need to *2 for one-sided. Default:
            - `[.005, .01, .05, .1]`
        `betas` : 1-power. Default: `[.05, .1, .2]`
    """),
    input='infile:file, ngroup1, ngroup2, ngroup3, ngroup4',
    output='outfile:file:{{i.infile | fn}}.power/{{i.infile | fn}}.ssize.txt, \
            outdir:dir:{{i.infile | fn}}.power',
    lang=opts.Rscript,
    args=Diot(
        rnames=True,
        plot=False,
        ngroup=2,
        intype='detailed',  # ratios or ratio,
        alphas=[.005, .01, .05, .1],  # two-sided, *2 if you want one-sided
        betas=[.05, .1, .2]
    )
)
