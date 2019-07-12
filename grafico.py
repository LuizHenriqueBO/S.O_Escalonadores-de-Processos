# import plotly.plotly as py
import plotly.figure_factory as ff
# from plotly import tools
# tools.set_credentials_file(username='hick', api_key='phFKCu1UETF03TXbu4Ni')
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot



def add_dados_diagrama_gantt(gp, tempo):
    gp.get_fila_finalizados().sort(key = lambda x: x.get_id())

    # print("executando")
    # for i in gp.get_fila_finalizados():
    #     print(i.lista_execucao)
    
    # print("bloqueado")
    # for i in gp.get_fila_finalizados():
    #     print(i.lista_bloqueado)

    # print("espera")
    # for i in gp.get_fila_finalizados():
    #     print(i.lista_espera)

    lista_dados = list()
    
    colors = {'execucao': 'rgb(0, 255, 0)',
            'espera': (1, 0.9, 0.16),
            'bloqueado': 'rgb(255, 0, 0)'}

    for processo in gp.get_fila_finalizados():
    

        # for pos in range(0, int(len(processo.lista_execucao)),2):
        #     dados = dict(
        #         Task=str(processo.get_id()),
        #         Start=str( processo.lista_execucao[pos]), 
        #         Finish=str( processo.lista_execucao[pos+1]), 
        #         Resource='execucao'
        #     )
        #     lista_dados.append(dados)
      


        # for pos in range(0, int(len(processo.lista_espera)),2):
        #     dados = dict(
        #         Task=str(processo.get_id()),
        #         Start=str( processo.lista_espera[pos]),
        #         Finish=str(processo.lista_espera[pos+1]),
        #         Resource='espera'
        #     )
        #     lista_dados.append(dados)


        for pos in range(0, int(len(processo.lista_bloqueado)),2):
            dados = dict(
                Task=str(processo.get_id()),
                Start=str(processo.lista_bloqueado[pos]), 
                Finish=str( processo.lista_bloqueado[pos+1]), 
                Resource='bloqueado'
            )
            lista_dados.append(dados)

        for pos in range(0, int(len(processo.lista_execucao)),2):
            dados = dict(
                Task=str(processo.get_id()),
                Start=str( processo.lista_execucao[pos]), 
                Finish=str( processo.lista_execucao[pos+1]), 
                Resource='execucao'
            )
            lista_dados.append(dados)

        for pos in range(0, int(len(processo.lista_espera)),2):
            dados = dict(
                Task=str(processo.get_id()),
                Start=str( processo.lista_espera[pos]),
                Finish=str(processo.lista_espera[pos+1]),
                Resource='espera'
            )
            lista_dados.append(dados)
        

 
    fig = ff.create_gantt(lista_dados , colors=colors, title="Diagrama de gantt",width=1350, 
    height=580, bar_width=0.4, index_col='Resource', showgrid_x= True, showgrid_y=True, show_colorbar=True, group_tasks=True)


    fig['layout'].update(legend=dict(orientation="h", font=dict(family='Arial-Black', size=13, color='#510')))
    fig['layout']['yaxis'].update({'title': 'ID DOS PROCESSOS', 'titlefont':{'family':'Arial-Black', 'size':13, 'color':'#510'}})
    fig['layout']['xaxis'].update({'title': 'CLOCK', 'titlefont':{'family':'Arial-Black', 'size':13, 'color':'#510'}})
    

    list_evals = list()
    lista_clock = list()
    for i in range(tempo):
        list_evals.append(i)
        lista_clock.append(str(i))

    fig['layout']['xaxis'].update({'type': 'linear'})
    fig['layout']['xaxis'].update({'ticks':'outside'})
    fig['layout']['xaxis'].update({'tickmode':'array'})
    # fig['layout']['xaxis'].update({'ticktext':lista_clock})
    fig['layout']['xaxis'].update({'tickvals':list_evals})
    fig['layout']['xaxis'].update({'rangeselector': None })
    # fig['layout']['xaxis'].update({'tickangle':90})
    fig['layout']['xaxis'].update({'showgrid':True})

    fig['layout']['yaxis'].update({'type': 'linear'})
    # fig['layout']['yaxis'].update({'ticks':'inside'})
    fig['layout']['yaxis'].update({'showgrid':True})
    
    
    print()
    # print(fig["layout"])

    plot(fig, filename='gantt-group-tasks-together')

#     fig = ff.create_gantt(dados, colors=cores, index_col='Resource', show_colorbar=True, group_tasks=True)
#     py.plot(fig, filename='gantt-group-tasks-together', world_readable=True)
