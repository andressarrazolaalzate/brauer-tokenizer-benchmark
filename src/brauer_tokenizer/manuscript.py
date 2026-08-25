"""Regression targets transcribed from the final 15-page manuscript."""
from __future__ import annotations

TABLE2 = {
    "BERT":       {"N_incl":23.436,"N_excl":21.436,"CB":68.308,"HB":3.142,"dim_Lambda":179.488,"delta_CB":6.000},
    "RoBERTa":    {"N_incl":22.880,"N_excl":20.880,"CB":66.640,"HB":3.118,"dim_Lambda":175.040,"delta_CB":6.000},
    "Mistral-7B": {"N_incl":24.366,"N_excl":23.366,"CB":71.098,"HB":3.183,"dim_Lambda":186.928,"delta_CB":3.000},
    "GPT-2":      {"N_incl":20.880,"N_excl":20.880,"CB":60.640,"HB":3.025,"dim_Lambda":159.040,"delta_CB":0.000},
    "Qwen2.5":    {"N_incl":21.328,"N_excl":21.328,"CB":61.984,"HB":3.050,"dim_Lambda":162.624,"delta_CB":0.000},
}
TABLE3_ENTROPY = {
    0:{"BERT":3.147,"RoBERTa":3.123,"Mistral-7B":3.188,"GPT-2":3.030,"Qwen2.5":3.055},
    1:{"BERT":3.142,"RoBERTa":3.118,"Mistral-7B":3.183,"GPT-2":3.025,"Qwen2.5":3.050},
    2:{"BERT":3.138,"RoBERTa":3.114,"Mistral-7B":3.179,"GPT-2":3.020,"Qwen2.5":3.046},
    3:{"BERT":3.135,"RoBERTa":3.111,"Mistral-7B":3.176,"GPT-2":3.017,"Qwen2.5":3.042},
}
TABLE3_GROWTH = {
    2:{"BERT":62.76,"RoBERTa":62.67,"Mistral-7B":62.92,"GPT-2":62.27,"Qwen2.5":62.36},
    3:{"BERT":122.60,"RoBERTa":122.33,"Mistral-7B":123.02,"GPT-2":121.24,"Qwen2.5":121.50},
}
TABLE4 = {
    1:{"CB":67,"HB":3.1303,"HB_type":2.8820,"delta_H":-0.2483,"dim_Lambda":176,"dim_Lambda_type":284,"ratio":1.61},
    2:{"CB":109,"HB":3.1264,"HB_type":2.8855,"delta_H":-0.2409,"dim_Lambda":462,"dim_Lambda_type":732,"ratio":1.58},
    3:{"CB":149,"HB":3.1231,"HB_type":2.8828,"delta_H":-0.2403,"dim_Lambda":884,"dim_Lambda_type":1388,"ratio":1.57},
}
