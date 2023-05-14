from flask import Flask, redirect, url_for, request, render_template, session
import random

from mod import Mod
from with_tolerance import paramsWT, proveWT_Flask

app = Flask(__name__, template_folder='html')


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

        int1 = -2 ** s * n + 1
        int2 = 2 ** s * n - 1
        r = {'r': random.randint(int1, int2), 'int1': int1, 'int2': int2}
        session['r'] = r

        E = (Mod(g, n) ** x * Mod(h, n) ** r['r']).x
        proof, ext_wt, ext_sa, ext_ssa, ext_sb, ext_ssb, ext_lia, ext_lib = proveWT_Flask(x, n, g, h, r['r'], a, b, E,
                                                                                          paramsWT(t, l, s))

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

        return redirect(url_for('sd'))
    else:
        return render_template('input.html')


@app.route('/prove', methods=['POST', 'GET'])
def sd():
    debug = False

    if request.method == 'POST':
        if request.form['prove'] == 'proof_sa':
            return redirect(url_for('proveS', proveS='proof_sa'))
        elif request.form['prove'] == 'proof_sb':
            return redirect(url_for('proveS', proveS='proof_sb'))
        elif request.form['prove'] == 'proof_lia':
            return redirect(url_for('proveLI', proveS='proof_lia'))
        elif request.form['prove'] == 'proof_lib':
            return redirect(url_for('proveLI', proveS='proof_lib'))
        elif request.form['prove'] == 'back':
            return redirect(url_for('input'))
    else:
        inputs = session['inputs']
        params = session['params']
        r = session['r']
        proof_wt = session['proof_wt']
        ext_wt = session['ext_wt']
        proof_sa = session['proof_sa']
        proof_sb = session['proof_sb']
        proof_lia = session['proof_lia']
        proof_lib = session['proof_lib']

        if debug:
            print('Input: {}\nparams: {}\nr: {}\nproof_wt: {}\next_wt: {}\nproof_sa: {}\nproof_sb: {}\nproof_lia: {}\nproof_lib: {}'.format(
                    inputs, params, r, proof_wt, ext_wt, proof_sa, proof_sb, proof_lia, proof_lib))

            print("\n\t---Types---\n")
            outputs = [inputs, params, r, proof_wt, ext_wt, proof_sa, proof_sb, proof_lia, proof_lib]
            for output in outputs:
                for element in output:
                    print(element, type(output[element]))

        return render_template('prove_sd.html', inputs=inputs, params=params, r=r, proof_wt=proof_wt, ext_wt=ext_wt,
                               proof_sa=proof_sa, proof_sb=proof_sb, proof_lia=proof_lia, proof_lib=proof_lib)


@app.route('/prove/<proveS>', methods=['POST', 'GET'])
def proveS(proveS):
    if request.method == 'POST':
        if request.form['proveS'] == 'proof_ss':
            if proveS == 'proof_sa':
                return redirect(url_for('proveSS', proveS=proveS, proveSS='proof_ssa'))
            elif proveS == 'proof_sb':
                return redirect(url_for('proveSS', proveS=proveS, proveSS='proof_ssb'))
        elif request.form['proveS'] == 'back':
            return redirect(url_for('sd'))
    else:
        inputs = session['inputs']
        ext_wt = session['ext_wt']
        params = session['params']
        r = session['r']

        if proveS == 'proof_sa':
            proof = session['proof_sa']
            ext_s = session['ext_sa']
            ext = {'x': ext_wt['xa1'], 'r1': ext_wt['ra1'], 'int1': r['int1'], 'int2': r['int2']}
        elif proveS == 'proof_sb':
            proof = session['proof_sb']
            ext_s = session['ext_sb']
            ext = {'x': ext_wt['xb1'], 'r1': ext_wt['rb1'], 'int1': r['int1'], 'int2': r['int2']}
        else:
            assert True, 'Prueba no encontrada'

        return render_template('prove_s.html', proof=proof, ext_s=ext_s, inputs=inputs, params=params, ext=ext)


@app.route('/prove/<proveS>/<proveSS>', methods=['POST', 'GET'])
def proveSS(proveS, proveSS):
    if request.method == 'POST':
        if request.form['proveSS'] == 'back':
            return redirect(url_for('proveS', proveS=proveS))
    else:
        inputs = session['inputs']
        ext_wt = session['ext_wt']
        params = session['params']

        if proveS == 'proof_sa':
            proof_s = session['proof_sa']
            ext_sa = session['ext_sa']
            ext_s = {'x': ext_wt['xa1'], 'r2': ext_sa['r2'], 'r3': ext_sa['r3'], 'E': ext_sa['E'], 'F': ext_sa['F']}
        elif proveS == 'proof_sb':
            proof_s = session['proof_sb']
            ext_sb = session['ext_sb']
            ext_s = {'x': ext_wt['xa1'], 'r2': ext_sb['r2'], 'r3': ext_sb['r3'], 'E': ext_sb['E'], 'F': ext_sb['F']}

        if proveSS == 'proof_ssa':
            ext = session['ext_ssa']
            proof = {'x': ext_s['x'], 'r1': ext_s['r3'], 'r2': ext_s['r2'], 'g1': ext_s['F'], 'g2': inputs['g'], 'h': inputs['h']}
        elif proveSS == 'proof_ssb':
            ext = session['ext_ssb']
            proof = {'x': ext_s['x'], 'r1': ext_s['r3'], 'r2': ext_s['r2'], 'g1': ext_s['F'], 'g2': inputs['g'], 'h': inputs['h']}

        return render_template('prove_ss.html', inputs=inputs, params=params, proof=proof, ext=ext, proof_s=proof_s)


@app.route('/prove/<prove>', methods=['GET'])
def proveLI(prove):
    return prove


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
