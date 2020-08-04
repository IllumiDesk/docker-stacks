# This mechanism allows us to import a package list.
# Source: https://discourse.julialang.org/t/building-a-dockerfile-with-packages/37272/2

using Pkg
pkg"add Colors"
pkg"add CSV"
pkg"add DelimitedFiles"
pkg"add GR"
pkg"add IJulia"
pkg"add ImageView"
pkg"add ImageInTerminal"
pkg"add FileIO"
pkg"add ImageFiltering"
pkg"add Images"
pkg"add ImageFeatures"
pkg"add LinearAlgebra"
pkg"add Plots"
pkg"add PyPlot"
pkg"add Random"
pkg"add GtkReactive"
pkg"add Roots"
pkg"add SymEngine"
pkg"add Statistics"
pkg"add TestImages"
pkg"add Plotly"
pkg"add Distributions"
pkg"add ProgressBars"
pkg"add https://github.com/VMLS-book/VMLS.jl"
pkg"add https://github.com/korsbo/Latexify.jl"
pkg"precompile"
