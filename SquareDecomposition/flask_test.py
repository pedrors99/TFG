from flask import Flask, redirect, url_for, request, render_template, session
import random

from mod import Mod
from with_tolerance import paramsWT, proveWT_Flask

app = Flask(__name__, template_folder='html')


@app.route('/sd', methods=['POST', 'GET'])
def sd():
    if request.method == 'POST':
        pass
    else:
        inputs = session['inputs']
        params = session['params']

        int1 = -2 ** params['s'] * inputs['n'] + 1
        int2 = 2 ** params['s'] * inputs['n'] - 1
        r = {'r': random.randint(int1, int2), 'int1': int1, 'int2': int2}
        session['r'] = r

        E = (Mod(inputs['g'], inputs['n']) ** inputs['x'] * Mod(inputs['h'], inputs['n']) ** r['r']).x
        proof, ext_wt, ext_sa, ext_ssa, ext_sb, ext_ssb, ext_lia, ext_lib =\
            proveWT_Flask(inputs['x'], inputs['n'], inputs['g'], inputs['h'], r['r'], inputs['a'], inputs['b'], E,
                          paramsWT(params['t'], params['l'], params['s']))

        proof_wt = {'E': int(E), 'Ea': int(proof.Ea), 'Eb': int(proof.Eb), 'Ea1': int(proof.Ea1),
                    'Ea2': int(proof.Ea2), 'Eb1': int(proof.Eb1), 'Eb2': int(proof.Eb2)}
        session['proof_wt'] = proof_wt
        session['ext_wt'] = ext_wt

        proof_sa = {'E': int(proof.proof_sa.E), 'F': int(proof.proof_sa.F),
                    'proof_c': int(proof.proof_sa.proof_ss.c), 'proof_D': int(proof.proof_sa.proof_ss.D),
                    'proof_D1': int(proof.proof_sa.proof_ss.D1), 'proof_D2': int(proof.proof_sa.proof_ss.D2)}
        session['proof_sa'] = proof_sa
        session['ext_sa'] = ext_sa
        session['ext_ssa'] = ext_ssa

        proof_sb = {'E': int(proof.proof_sb.E), 'F': int(proof.proof_sb.F),
                    'proof_c': int(proof.proof_sb.proof_ss.c), 'proof_D': int(proof.proof_sb.proof_ss.D),
                    'proof_D1': int(proof.proof_sb.proof_ss.D1), 'proof_D2': int(proof.proof_sb.proof_ss.D2)}
        session['proof_sb'] = proof_sb
        session['ext_sb'] = ext_sb
        session['ext_ssb'] = ext_ssb

        proof_lia = {'C': int(proof.proof_lia.C), 'D1': int(proof.proof_lia.D1), 'D2': int(proof.proof_lia.D2),
                     'c': int(proof.proof_lia.c)}
        session['proof_lia'] = proof_lia
        session['ext_lia'] = ext_lia

        proof_lib = {'C': int(proof.proof_lib.C), 'D1': int(proof.proof_lib.D1), 'D2': int(proof.proof_lib.D2),
                     'c': int(proof.proof_lib.c)}
        session['proof_lib'] = proof_lib
        session['ext_lib'] = ext_lib

        if False:
            print('Input: {}\nparams: {}\nr: {}\nproof_wt: {}\next_wt: {}\nproof_sa: {}\nproof_sb: {}\nproof_lia: {}\nproof_lib: {}'.format(
                    inputs, params, r, proof_wt, ext_wt, proof_sa, proof_sb, proof_lia, proof_lib))

            print("\n\t---Types---\n")
            outputs = [inputs, params, r, proof_wt, ext_wt, proof_sa, proof_sb, proof_lia, proof_lib]
            for output in outputs:
                for element in output:
                    print(element, type(output[element]))

        return render_template('sd.html', inputs=inputs, params=params, r=r, proof_wt=proof_wt, ext_wt=ext_wt,
                               proof_sa=proof_sa, proof_sb=proof_sb, proof_lia=proof_lia, proof_lib=proof_lib)


@app.route('/', methods=['POST', 'GET'])
def input():
    if request.method == 'POST':
        x = int(request.form['x'])
        n = int(request.form['n'])

        a = int(request.form['a'])
        b = int(request.form['b'])

        g = int(request.form['g'])
        h = int(request.form['h'])

        t = int(request.form['t'])
        l = int(request.form['l'])
        s = int(request.form['s'])

        session['inputs'] = {'x': x, 'n': n, 'a': a, 'b': b, 'g': g, 'h': h}
        session['params'] = {'t': t, 'l': l, 's': s}

        return redirect(url_for('sd'))
    else:
        return render_template('input.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
