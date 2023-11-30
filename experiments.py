from main_objects import *

def params_search(method_navigation: str = 'kalman_filter rv', t_integrate: float = 1e5, dt: float = 10.,
                  aero: bool = False,):
    min_discrepancy = 1e10
    count = 0
    best_params = []
    d_list = [1e-5, 1e-4, 3e-4, 1e-3, 3e-3]
    q_list = [1e-12, 1e-11, 1e-10, 1e-9, 1e-8]
    r_list = [1e-4, 1e-2]
    p1_list = [1e-12, 1e-10, 1e-8]
    p2_list = [1e-12, 1e-10, 1e-8]
    # p3_list = [1e-10, 1e-8]
    # [1e-12, 1e-10, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    N = len(d_list) * len(q_list) * len(r_list) * len(p1_list) * len(p2_list)  # * len(p3_list)
    time_begin = datetime.now()
    for q in q_list:
        for r in r_list:
            for p1 in p1_list:
                for p2 in p2_list:
                    # for p3 in p3_list:
                    tmp = 0
                    count += 1
                    if count % 10 == 0:
                        print(f"Поиск коэффициентов фильтра Калмана {count}/{N}={int(100 * count / N)}%, " +
                              real_workload_time(n=count, n_total=N,
                                                 time_begin=time_begin, time_now=datetime.now()))
                    for _ in range(1):
                        o = Objects(n_c=1, n_f=1,
                                    kalman_coef={'q': q, 'p': [p1, p2, p2], 'r': r},
                                    model_c='1U', dt=dt, start_navigation='near',  # random perfect
                                    start_navigation_tolerance=0.98,
                                    method_navigation=method_navigation, if_any_print=False)
                        o.f.gain_mode = ['isotropic', 'ellipsoid', '1 antenna', '2 antennas'][3]
                        o.f.ellipsoidal_signal = 0.99
                        o.p.is_aero = aero
                        o.p.integrate(t=t_integrate)

                        tmp += np.sum(np.abs(np.array(o.c.real_dist[0][0]) - np.array(o.c.calc_dist[0][0])))
                    if tmp < min_discrepancy:
                        min_discrepancy = tmp
                        best_params = [q, p1, p2, p2, r]
    print(f"Подходящие параметры: 'q': {best_params[0]}, 'p': {best_params[1:4]}, 'r': {best_params[4]}")
    print(f"best_params={best_params}")
    return best_params


params_search()
