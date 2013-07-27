
import usolib


if __name__ == "__main__":
    K = 4
    usos_itr = usolib.uso.all_by_states(K)
    usos = usolib.fst_helpers.uniq(usos_itr)
    fd = open("/home/vitor/usos.txt", "w")

    for uso in usos:
        print >> fd, ", ".join(str(i) for i in uso.get_edges())
    
