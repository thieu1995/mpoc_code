import matplotlib.pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams["font.family"] = "Arial"
import numpy as np

def circle_graph(market_share_dpos1, market_share_dpos2, market_share_dpos3, 
                 market_share_mdpos_75_1, market_share_mdpos_75_2, market_share_mdpos_75_3,
                 market_share_mdpos_100_1, market_share_mdpos_100_2, market_share_mdpos_100_3,
                 market_share_mdpos_125_1, market_share_mdpos_125_2, market_share_mdpos_125_3):
    market_share_dpos1 = sorted(market_share_dpos1)
    market_share_dpos2 = sorted(market_share_dpos2)
    market_share_dpos3 = sorted(market_share_dpos3)

    market_share_mdpos_75_1 = sorted(market_share_mdpos_75_1)
    market_share_mdpos_75_2 = sorted(market_share_mdpos_75_2)
    market_share_mdpos_75_3 = sorted(market_share_mdpos_75_3)

    market_share_mdpos_100_1 = sorted(market_share_mdpos_100_1)
    market_share_mdpos_100_2 = sorted(market_share_mdpos_100_2)
    market_share_mdpos_100_3 = sorted(market_share_mdpos_100_3)

    market_share_mdpos_125_1 = sorted(market_share_mdpos_125_1)
    market_share_mdpos_125_2 = sorted(market_share_mdpos_125_2)
    market_share_mdpos_125_3 = sorted(market_share_mdpos_125_3)
    fig = plt.figure(figsize=(12, 11))
    radius = 1.7
    label_algo = -1.5
    font_dict = {'fontsize': 20}
    # fig.suptitle("Experiments show dispersion leader across the network", fontsize=14, y=0.95)
    ax = plt.subplot2grid((4, 3),(0, 0))
    # ax.update(wspace = 0.5, hspace = 0.5)
    ax.set_title("DPoS", fontdict=font_dict, loc="left", y=0.4, x=label_algo)
    ax.pie(market_share_dpos1, radius=radius)
    ax1 = plt.subplot2grid((4, 3), (0, 1))
    # ax1.set_title("Scenario 2", y=-0.1)
    ax1.pie(market_share_dpos2, radius=radius)
    ax2 = plt.subplot2grid((4, 3), (0, 2))
    # ax2.set_title("Scenario 3", y=-0.1)
    ax2.pie(market_share_dpos3, radius=radius)

    ax3 = plt.subplot2grid((4, 3),(1, 0))
    ax3.set_title("MPoC (n=75)", fontdict=font_dict, loc="left", y=0.4, x=label_algo)
    ax3.pie(market_share_mdpos_75_1, radius=radius)
    ax4 = plt.subplot2grid((4, 3), (1, 1))
    ax4.pie(market_share_mdpos_75_2, radius=radius)
    ax5 = plt.subplot2grid((4, 3), (1, 2))
    ax5.pie(market_share_mdpos_75_3, radius=radius)

    ax6 = plt.subplot2grid((4, 3),(2, 0))
    ax6.set_title("MPoC (n=100)", fontdict=font_dict, loc="left", y=0.4, x=label_algo)
    ax6.pie(market_share_mdpos_100_1, radius=radius)
    ax7 = plt.subplot2grid((4, 3), (2, 1))
    ax7.pie(market_share_mdpos_100_2, radius=radius)
    ax8 = plt.subplot2grid((4, 3), (2, 2))
    ax8.pie(market_share_mdpos_100_3, radius=radius)

    ax9 = plt.subplot2grid((4, 3),(3, 0))
    ax9.set_title("Scenario 1", fontdict=font_dict, y=-0.4)
    ax9.set_title("MPoC (n=125)", fontdict=font_dict, loc="left", y=0.4, x=label_algo)
    ax9.pie(market_share_mdpos_125_1, radius=radius)
    ax10 = plt.subplot2grid((4, 3), (3, 1))
    ax10.set_title("Scenario 2", fontdict=font_dict, y=-0.4)
    ax10.pie(market_share_mdpos_125_2, radius=radius)
    ax11 = plt.subplot2grid((4, 3), (3, 2))
    ax11.set_title("Scenario 3", fontdict=font_dict, y=-0.4)
    ax11.pie(market_share_mdpos_125_3, radius=radius)
    plt.tight_layout(pad=0.4, w_pad=2.0, h_pad=1.5)
    # print('0.4')
    # plt.show()

    # plt.title("The network scenario has 500 nodes")
    # plt.
    # plt.title('A tale of 2 subplots')
    # plt.ylabel('Damped oscillation')


    # plt.subplot(1, 3, 2, label="Script 2")
    # plt.pie(market_share2)
    # plt.xlabel('time (s)')
    # plt.ylabel('Undamped')
    # plt.subplot(1, 3, 3)
    # plt.pie(market_share3)

    plt.savefig('decentralized_nodes_235_2.pdf')
    plt.savefig('decentralized_nodes_235_2.png')
    
    # plt.pie(market_share3)
    # plt.show()

def bar_chart(num_leader_arr):
    # x = np.arange(len(num_leader_arr))
    # print(x)
    x = [0]
    width = 0.1
    fig, ax = plt.subplots()
    # fig.suptitle("Experiments show the number of nodes on the network becoming a leader", fontsize=11, y=0.95)
    rects1 = ax.bar(0.1, num_leader_arr[0], width, color='blue', label='scenario 1')
    rects1 = ax.bar(0.2, num_leader_arr[1], width, color='green', label='scenario 2')
    rects1 = ax.bar(0.3, num_leader_arr[2], width, color='red', label='scenario 3')

    rects1 = ax.bar(0.5, num_leader_arr[3], width, color='blue')
    rects1 = ax.bar(0.6, num_leader_arr[4], width, color='green')
    rects1 = ax.bar(0.7, num_leader_arr[5], width, color='red')

    rects1 = ax.bar(0.9, num_leader_arr[6], width, color='blue')
    rects1 = ax.bar(1.0, num_leader_arr[7], width, color='green')
    rects1 = ax.bar(1.1, num_leader_arr[8], width, color='red')
    # rects1 = ax.bar(0.4, num_leader_arr[3], width, color='gray', label='200 nodes with scenario 4')
    # rects1 = ax.bar(0.5, num_leader_arr[4], width, color='brown', label='200 nodes with scenario 5')
    # rects1 = ax.bar(0.6, num_leader_arr[5], width, color='orange', label='200 nodes with scenario 6')
    
    rects1 = ax.bar(1.3, num_leader_arr[9], width, color='blue')
    rects1 = ax.bar(1.4, num_leader_arr[10], width, color='green')
    rects1 = ax.bar(1.5, num_leader_arr[11], width, color='red')
    # rects1 = ax.bar(1.1, num_leader_arr[9], width, color='gray', label='500 nodes with scenario 4')
    # rects1 = ax.bar(1.2, num_leader_arr[10], width, color='brown', label='500 nodes with scenario 5')
    # rects1 = ax.bar(1.3, num_leader_arr[11], width, color='orange', label='500 nodes with scenario 6')
    plt.legend()
    # ax.set_xticks(x)
    ax.set_xticklabels(['', '', 'DPoS', '', 'MPoC (n=75)', '', 'MPoC (n=100)', '','MPoC (n=125)', ''])
    # plt.show()
    plt.savefig('arial_num_leader_time_235.pdf')
    plt.savefig('arial_num_leader_time_235.png')
