# only works on 960x540
from universal_small_res import *

Path_to_script = ''
def read_config_file():
    print('\tread_config_file()')
    file = open('config.txt')
    tmp = file.readline().strip()
    while tmp != '':
        tmp = str(tmp).split()
        if tmp[0] == 'path':
            set_path(tmp[1])
        if tmp[0] == 'path_to_script':
            global Path_to_script
            Path_to_script = (tmp[1])
            set_path_to_script(Path_to_script)
        tmp = file.readline()

start_time = time.time()

# INTERFACE HELPER
def image_read_asteroid(image1):
    print('\t\timage_read_asteroid()')
    min_value = 10000
    best_match = ''
    for asteroid_file in os.listdir(Path_to_script + 'assets\\asteroids\\'):
        image2 = cv.imread(Path_to_script + 'assets\\asteroids\\' + asteroid_file)
        value = image_compare_text(image1, image2)
        if value < min_value:
            min_value = value
            best_match = asteroid_file
    return best_match[:-4]
def get_list_asteroid():
    print('\tget_list_asteroid()')
    # swap_filter('ining')
    # click filter element to expand filter
    device_click_filter_block()
    list_ast = []

    device_update_cs()

    # create a list of all anomaly locations (on screen)
    x, y, w, h = 731, 49, 10, 474
    img_ast = cv.imread(Path_to_script + 'assets\\ast.png')
    crop_img = get_cs_cv()[y:y + h, x:x + w]
    crop_img = image_remove_dark(crop_img, 250)
    result = cv.matchTemplate(crop_img, img_ast, cv.TM_CCORR_NORMED)
    threshold = 0.92
    loc = np.where(result >= threshold)
    # black magic do not touch
    previous_point_y = -10
    for pt in zip(*loc[::-1]):
        # ignore double results
        if pt[1] > previous_point_y + 10:
            previous_point_y = pt[1]
            # icon offset, size of text field
            y_text, x_text = pt[1] - 12 + y, pt[0] + 59 + x
            crop_img = get_cs_cv()[y_text:y_text + 33, x_text:x_text + 117]

            # template gen
            # remove darker pixels, seems to be a bad idea
            # crop_img = remove_bright_pix(crop_img, 75)
            # cv.imwrite('test.png', crop_img)
            # cv.imshow('.', crop_img)
            # cv.waitKey()

            list_ast.append([image_read_asteroid(crop_img), x_text - 40, y_text - 4, 150, 35])
            cv.rectangle(get_cs_cv(), (x_text - 40, y_text-4), (x_text - 40 + 150, y_text-4 + 35), (0, 0, 255), 2)
    # cv.imshow('.', CS_cv)
    # cv.waitKey()
    return list_ast
def get_good_asteroid_from_list(ast_list):
    print('\tget_good_asteroid_from_list()')
    file = open(Path_to_script + 'assets\\ore_pref.txt')
    tmp = file.readline().strip()
    while tmp != '':
        for ast in ast_list:
            if ast[0] == tmp:
                return ast
        tmp = file.readline().strip()

    # swipe down
    device_click_rectangle(740, 46, 161, 269)
    device_swipe_from_circle(822, 493, 20, 400, 3)
    ast_list = get_list_asteroid()

    file = open(Path_to_script + 'assets\\ore_pref.txt')
    tmp = file.readline().strip()
    while tmp != '':
        for ast2 in ast_list:
            if ast2[0] == tmp:
                return ast2
        tmp = file.readline().strip()
    if get_cargo() > 90:
        mining_return(0)
        quit()
    set_filter('esc', 1)
    warp_in_system(int(np.random.default_rng().random() * 3.99 + 1), 0, 1, 'ining')
    mining_in_belt()
    quit()

# TASKS
def mine():
    print(' mine')
    if get_eco_mode():
        device_toggle_eco_mode()

    activate_the_modules('prop')

    # sometimes, ancient thing spawns, slow down
    loot_green = [48, 94, 87]
    x, y = 362, 457
    tmp = get_filter_icon('wreck')
    if tmp != 0:
        device_click_rectangle(tmp[0] + 1, tmp[1] + 1, 1, 1)
        wait_and_watch_out(2)
        filter_action(1, 2, 5)

        time.sleep(4)
        device_update_cs()
        if compare_colors(loot_green, get_cs_cv()[y][x]) < 15:
            device_click_circle(x, y, 15)
        if get_speed() > 50:
            device_click_circle(353, 454, 20)
            wait_and_watch_out(14)
        time.sleep(2)
        device_update_cs()
        
    if get_speed() > 50:
        device_click_circle(353, 454, 20)
        wait_and_watch_out(6)
    # catch
    if compare_colors(loot_green, get_cs_cv()[y][x]) < 15:
        device_click_circle(x, y, 15)

    # select some asteroid
    set_filter('inin', 0)
    device_update_cs()
    tmp = get_filter_icon('asteroid')
    activate_the_modules('prop')
    if tmp == 0:
        set_filter('esc', 0)
        warp_in_system(int(np.random.default_rng().random() * 2.99 + 2), 0, 1, 'ining')
        mining_in_belt()
        quit()
    device_click_rectangle(tmp[0] + 1, tmp[1] + 1, 1, 1)
    device_update_cs()
    a_list = get_list_asteroid()
    asteroid = get_good_asteroid_from_list(a_list)
    print(' mining ', asteroid[0])

    asteroid.pop(0)

    wait_and_watch_out(4)
    # click filter element to expand filter
    if asteroid[1] > 260:
        device_click_filter_block()
    time.sleep(1)
    device_click_rectangle(asteroid[0], asteroid[1], asteroid[2], asteroid[3])
    time.sleep(0.5)
    device_click_rectangle(asteroid[0] - 185, min(315, asteroid[1]), asteroid[2], asteroid[3])

    # click filter element to expand filter
    if asteroid[1] > 260:
        device_click_filter_block()
    time.sleep(0.5)
    device_click_rectangle(asteroid[0], asteroid[1], asteroid[2], asteroid[3])
    time.sleep(0.5)
    device_click_rectangle(asteroid[0] - 185, min(315, asteroid[1]) + 58, asteroid[2], asteroid[3])
    wait_and_watch_out(4)
def wait_and_watch_out(sec):
    print('\twait_and_watch_out')
    for i in range(int(sec/2)):
        device_update_cs()
        if get_filter_icon('all_ships') != 0 or get_criminal() != 0:
            activate_autopilot(1)
            if get_bait() == 1:
                subprocess.call(["D:\Program Files\AutoHotkey\AutoHotkey.exe",
                                 "E:\\Eve_Echoes\\Bot\\ahk_scripts\\call_paul.ahk"])
                playsound(Path_to_script + 'assets\\sounds\\bell.wav')
                print('trap card activated')
                device_toggle_eco_mode()
                time.sleep(3)
                mining_return(1)
                quit()
            mining_return(1)
            quit()
        time.sleep(2)
def farm_tracker(got_ganked):
    print('\tfarm_tracker', got_ganked)
    # intended to be called when dumping cargo
    # t5med = 653k with frig in end
    global time_stamp_farming
    if not got_ganked:
        count = time.time()-time_stamp_farming
        string = get_name() + ': ' + str(datetime.datetime.utcnow()+datetime.timedelta(hours=2)) + '\n' + str(int(count/60)) + 'm ' + str(int(count - int(count/60)*60)) + 's\n\n'
        absolutely_professional_database = open('E:\\Eve_Echoes\\Bot\\professional_database.txt', 'a')
        absolutely_professional_database.write(string)
        absolutely_professional_database.close()

    time_stamp_farming = time.time()


# STATES
def mining_from_station():
    print('\tmining_from_station()')
    undock_and_modules()
    activate_filter_window()
    time.sleep(1)

    set_filter('esc', 0)

    time.sleep(1)
    warp_in_system(int(np.random.default_rng().random() * 3.99 + 1), 0, 1, 'ining')
    mining_in_belt()
# todo
def mining_in_belt():
    print(' mining_in_belt()')
    device_update_cs()

    # check if time is up
    if get_cargo() > 90:
        deactivate_the_modules('harvest')
        mining_return(0)
        return

    # check if mining equipment is busy/ easily activated
    # if not, deactivate eco_state and start mining
    miners_active = 1
    stop = 0
    for module in get_module_list():
        if module[1] == 'harvest' and stop == 0:
            if not get_module_is_active(module):
                activate_module(module)
                if get_eco_mode():
                    wait_and_watch_out(10)
                else:
                    wait_and_watch_out(2)
                device_update_cs()
                if not get_module_is_active(module):
                    miners_active = 0
                    stop = 1
    if not miners_active:
        if get_cargo() > 75:
            device_toggle_eco_mode()
            mining_return(0)
            return
        if get_is_locked(1):
            wait_and_watch_out(20)
            device_swipe_from_circle(435, 265, 250, 1, 0)
            mining_in_belt()
            return
        if get_eco_mode():
            device_toggle_eco_mode()
        wait_and_watch_out(4)
        print('searching for asteroid')
        mine()
        mining_in_belt()
        return
    else:
        # set state to stable, autopilot
        if not get_eco_mode():
            if not get_autopilot():
                print('setting path home')
                time.sleep(2)
                set_home()
            device_toggle_eco_mode()
            mining_in_belt()
            return
    wait_and_watch_out(25)
    mining_in_belt()
def mining_return(got_ganked):
    print(' mining_return()')
    # activate autopilot and run (maybe i got ganked?)
    escape_autopilot()
    # usually, it spam clicks esc modules, which creates a warning
    device_click_rectangle(246, 269, 77, 73)
    if got_ganked == 1:
        print('got ganked')
        ding_when_ganked()
        save_screenshot()
    device_update_cs()

    catch_bad_eco_mode(1)

    print(' \tchecking if dead')
    if get_is_capsule() or get_is_in_station():
        absolutely_professional_database = open('E:\\Eve_Echoes\\Bot\\professional_database.txt', 'a')
        absolutely_professional_database.write(
            get_name() + ' died at:' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370)) + '\n\n')
        absolutely_professional_database.close()
        quit()
    else:
        print('going home')
        # wait until autopilot gone
        wait_end_navigation(20)

        print('arriving')
        # dump ressources
        global start_time
        if start_time > time.time() + 10000:
            start_time = time.time()
            dump_both()
        else:
            dump_ore()
        farm_tracker(got_ganked)
        # repeat?
    if get_repeat() == 0:
        playsound(Path_to_script + 'assets\\sounds\\bell.wav')
        quit()
    if got_ganked == 1:
        time.sleep(get_safety_time())

    # catch
    if get_is_in_station() == 0:
        click_close_inv_window()
    if get_is_in_station() == 0:
        click_close_inv_window()

    mining_from_station()
    return
def test_esc():
    set_filter('ing', 0)
    device_toggle_eco_mode()
    wait_and_watch_out(200)
    device_toggle_eco_mode()
    mining_return(0)
    print(' test_esc()')

def mining_from_station_in_null():
    print(' mining_from_station_in_null()')
    # set destination
    set_pi_planet_for_autopilot(get_planet())
    # wait until autopilot gone
    wait_end_navigation(20)
    print('undocking')
    device_click_rectangle(817, 165, 111, 26)
    time.sleep(15)

    print('calibrating')
    device_update_cs()
    activate_filter_window()
    time.sleep(1)
    update_modules()

    print('going to system')
    device_update_cs()
    # activate autopilot
    activate_autopilot(0)
    # wait until autopilot gone
    wait_end_navigation(20)

    print('todo')
    # todo

# STARTS
def main():
    interface_show_player()
    mining_from_station()
def custom():
    while 1:
        device_update_cs()
        print(get_cargo())
        time.sleep(2)


read_config_file()
config_uni()
if get_start() == 'main':
    main()
if get_start() == 'custom':
    custom()
