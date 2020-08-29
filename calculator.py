import random
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
test_time = 3000


def simulate_play(winning_rate, total_winning_needed, star_bounce, have_five_to_one):
    total_count = 0
    star_count = 0
    consist_winning_count = 0
    while(star_count < total_winning_needed and total_count <= 450):
        r = random.randint(1, 100)
        total_count += 1
        if(r <= 100 * winning_rate):
            consist_winning_count += 1
            star_bounce = (star_bounce - int(star_count / 15)) if (star_bounce - int(star_count / 15)) >= 1 else 1

            five_to_one = total_winning_needed - star_count <= 15 and have_five_to_one
            if(consist_winning_count >= 3 and not five_to_one):
                star_count += 2 * star_bounce
            else:
                star_count += star_bounce
        else:
            consist_winning_count = 0
            if not star_count % 15 == 0:
                star_count -= 1

    return total_count


def show_figure(all_total_counts, total_winning_needed, star_bounce, winning_rate, have_five_to_one):

    x = all_total_counts

    fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(6, 10))

    ax0.hist(x[0], 40, density=1, histtype='stepfilled',
             facecolor='green', alpha=0.3)
    ax0.hist(x[1], 40, density=1, histtype='stepfilled',
             facecolor='yellow', alpha=0.3)
    ax0.hist(x[2], 40, density=1, histtype='stepfilled',
             facecolor='blue', alpha=0.3)

    ax1.hist(x[0], 100, density=1, histtype='stepfilled',
             facecolor='green', alpha=0.3, cumulative=True, rwidth=0.8)
    ax1.hist(x[1], 100, density=1, histtype='stepfilled',
             facecolor='yellow', alpha=0.3, cumulative=True, rwidth=0.8)
    ax1.hist(x[2], 100, density=1, histtype='stepfilled',
             facecolor='blue', alpha=0.3, cumulative=True, rwidth=0.8)

    ax0.set_title('--PDF & CDF-- \nStars needed: ' + str(total_winning_needed) +
                  '  Star bounce: ' + str(star_bounce) +
                  '  Win rate:  ' + str(winning_rate) + '±0.03' +
                  '\nWill go through Diamond5 to Legendary: ' + str(have_five_to_one) +
                  '\n')
    # ax1.set_title('--CDF-- \nStars needed: ' + str(total_winning_needed) +
    #               '\nStar bounce: ' + str(star_bounce) +
    #               '\nWin rate:  ' + str(winning_rate) + '±0.03' +
    #               '\nWill go through Diamond5 to Legendary: ' + str(have_five_to_one))
    fig.subplots_adjust(hspace=0.4)

    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims

    return imd

    # plt.savefig('./templates/pic/' + str(file_id) + '.png')


def run(total_winning_needed, star_bounce, winning_rate, have_five_to_one):
    all_total_counts = [[], [], []]
    COMPARE_NUM = 3
    UNCERTAINITY = 0.03
    total_winning_needed = int(total_winning_needed)
    star_bounce = int(star_bounce)

    winning_rate = float(winning_rate) / 100

    winning_rates = [winning_rate + UNCERTAINITY, winning_rate, winning_rate - UNCERTAINITY]

    for ii in range(test_time):        
        for jj in range(COMPARE_NUM):
            total_count = simulate_play(winning_rates[jj], total_winning_needed, star_bounce, have_five_to_one)
            all_total_counts[jj].append(total_count)

    imd = show_figure(all_total_counts, total_winning_needed, star_bounce, winning_rate, have_five_to_one)
    return imd

