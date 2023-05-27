from flask import Flask, redirect, url_for, request, render_template, session, flash
import random

from mod import Mod
from with_tolerance import paramsWT, proveWT_Flask, proofWT, verifyWT_Flask
from square import paramsS, proofS, verifyS_Flask
from same_secret import paramsSS, proofSS, verifySS_Flask
from interval import paramsLI, proofLI, verifyLI_Flask

app = Flask(__name__, template_folder='html')


@app.route('/', methods=['POST', 'GET'])
def input():
    if request.method == 'POST':
        cont = int(request.form['continue'])

        if cont:
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

            return redirect(url_for('proveSD'))
        else:
            return render_template('input.html')
    else:
        return render_template('input.html')


def modifyResults():
    proof_wt = session['proof_wt']
    proof_wt["Ea"] = int(request.form['Ea'])
    proof_wt["Ea1"] = int(request.form['Ea1'])
    proof_wt["Ea2"] = int(request.form['Ea2'])

    proof_wt["Eb"] = int(request.form['Eb'])
    proof_wt["Eb1"] = int(request.form['Eb1'])
    proof_wt["Eb2"] = int(request.form['Eb2'])
    session.pop('proof_wt')
    session['proof_wt'] = proof_wt

    proof_sa = session['proof_sa']
    proof_sa["E"] = int(request.form['Ea1'])
    proof_sa["F"] = int(request.form['proof_sa.F'])
    proof_sa["proof_c"] = int(request.form['proof_sa.proof_c'])
    proof_sa["proof_D"] = int(request.form['proof_sa.proof_D'])
    proof_sa["proof_D1"] = int(request.form['proof_sa.proof_D1'])
    proof_sa["proof_D2"] = int(request.form['proof_sa.proof_D2'])
    session.pop('proof_sa')
    session['proof_sa'] = proof_sa

    proof_sb = session['proof_sb']
    proof_sb["E"] = int(request.form['Eb1'])
    proof_sb["F"] = int(request.form['proof_sb.F'])
    proof_sb["proof_c"] = int(request.form['proof_sb.proof_c'])
    proof_sb["proof_D"] = int(request.form['proof_sb.proof_D'])
    proof_sb["proof_D1"] = int(request.form['proof_sb.proof_D1'])
    proof_sb["proof_D2"] = int(request.form['proof_sb.proof_D2'])
    session.pop('proof_sb')
    session['proof_sb'] = proof_sb

    proof_lia = session['proof_lia']
    proof_lia["C"] = int(request.form['proof_lia.C1'])
    proof_lia["D1"] = int(request.form['proof_lia.D1'])
    proof_lia["D2"] = int(request.form['proof_lia.D2'])
    proof_lia["c"] = int(request.form['proof_lia.c2'])
    session.pop('proof_lia')
    session['proof_lia'] = proof_lia

    proof_lib = session['proof_lib']
    proof_lib["C"] = int(request.form['proof_lib.C1'])
    proof_lib["D1"] = int(request.form['proof_lib.D1'])
    proof_lib["D2"] = int(request.form['proof_lib.D2'])
    proof_lib["c"] = int(request.form['proof_lib.c2'])
    session.pop('proof_lib')
    session['proof_lib'] = proof_lib


@app.route('/prove', methods=['POST', 'GET'])
def proveSD():
    debug = False

    if request.method == 'POST':
        modifyResults()
        if request.form['prove'] == 'proof_sa':
            return redirect(url_for('proveS', proveS='proof_sa'))
        elif request.form['prove'] == 'proof_sb':
            return redirect(url_for('proveS', proveS='proof_sb'))

        elif request.form['prove'] == 'proof_lia':
            return redirect(url_for('proveLI', proveLI='proof_lia'))
        elif request.form['prove'] == 'proof_lib':
            return redirect(url_for('proveLI', proveLI='proof_lib'))

        elif request.form['prove'] == 'verifier':
            return redirect(url_for('verifySD'))
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


@app.route('/verify', methods=['POST', 'GET'])
def verifySD():
    if request.method == 'POST':
        if request.form['verify'] == 'verify_lia':
            return redirect(url_for('verifyLI', verifyLI='verify_lia'))
        elif request.form['verify'] == 'verify_lib':
            return redirect(url_for('verifyLI', verifyLI='verify_lib'))
        elif request.form['verify'] == 'verify_sa':
            return redirect(url_for('verifyS', verifyS='verify_sa'))
        elif request.form['verify'] == 'verify_sb':
            return redirect(url_for('verifyS', verifyS='verify_sb'))
    else:
        inputs = session['inputs']
        params = session['params']

        proof_wt = session['proof_wt']
        proof_sa = session['proof_sa']
        proof_sb = session['proof_sb']
        proof_lia = session['proof_lia']
        proof_lib = session['proof_lib']

        params_ = paramsWT(params['t'], params['l'], params['s'])

        proof_ssa_ = proofSS(proof_sa['proof_c'], proof_sa['proof_D'], proof_sa['proof_D1'], proof_sa['proof_D2'])
        proof_sa_ = proofS(proof_sa['E'], proof_sa['F'], proof_ssa_)

        proof_ssb_ = proofSS(proof_sb['proof_c'], proof_sb['proof_D'], proof_sb['proof_D1'], proof_sb['proof_D2'])
        proof_sb_ = proofS(proof_sb['E'], proof_sb['F'], proof_ssb_)

        proof_lia_ = proofLI(proof_lia['C'], proof_lia['D1'], proof_lia['D2'], proof_lia['c'])

        proof_lib_ = proofLI(proof_lib['C'], proof_lib['D1'], proof_lib['D2'], proof_lib['c'])

        proof = proofWT(proof_wt['Ea'], proof_wt['Eb'], proof_wt['Ea1'], proof_wt['Ea2'], proof_wt['Eb1'],
                        proof_wt['Eb2'], proof_sa_, proof_sb_, proof_lia_, proof_lib_)

        result, ext = verifyWT_Flask(inputs['n'], inputs['g'], inputs['h'], inputs['b'], proof, params_)

        return render_template('verify_sd.html', inputs=inputs, params=params, proof_wt=proof_wt, proof_sa=proof_sa,
                               proof_sb=proof_sb, proof_lia=proof_lia, proof_lib=proof_lib, result=int(result), ext=ext)


@app.route('/prove/proveS/<proveS>', methods=['POST', 'GET'])
def proveS(proveS):
    if request.method == 'POST':
        if request.form['proveS'] == 'proof_ss':
            if proveS == 'proof_sa':
                return redirect(url_for('proveSS', proveS=proveS, proveSS='proof_ssa'))
            elif proveS == 'proof_sb':
                return redirect(url_for('proveSS', proveS=proveS, proveSS='proof_ssb'))

        elif request.form['proveS'] == 'verifyS':
            if proveS == 'proof_sa':
                return redirect(url_for('verifyS', verifyS='verify_sa'))
            elif proveS == 'proof_sb':
                return redirect(url_for('verifyS', verifyS='verify_sb'))
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


@app.route('/verify/verifyS/<verifyS>',  methods=['POST', 'GET'])
def verifyS(verifyS):
    if request.method == 'POST':
        if request.form['verifyS'] == 'verify_ss':
            if verifyS == 'verify_sa':
                return redirect(url_for('verifySS', verifyS=verifyS, verifySS='verify_ssa'))
            elif verifyS == 'verify_sb':
                return redirect(url_for('verifySS', verifyS=verifyS, verifySS='verify_ssb'))
    else:
        inputs = session['inputs']

        if verifyS == 'verify_sa':
            proof = session['proof_sa']
        elif verifyS == 'verify_sb':
            proof = session['proof_sb']

        proof_ss = proofSS(proof['proof_c'], proof['proof_D'], proof['proof_D1'], proof['proof_D2'])
        proof_ = proofS(proof['E'], proof['F'], proof_ss)

        result = verifyS_Flask(inputs['n'], inputs['g'], inputs['h'], proof_)

        return render_template('verify_s.html', inputs=inputs, proof=proof, result=int(result), res=result)


@app.route('/prove/proveS/<proveS>/proveSS/<proveSS>', methods=['POST', 'GET'])
def proveSS(proveS, proveSS):
    if request.method == 'POST':
        if request.form['proveSS'] == 'verifySS':
            if proveS == 'proof_sa':
                return redirect(url_for('verifySS', verifyS='verify_sa', verifySS='verify_ssa'))
            elif proveS == 'proof_sb':
                return redirect(url_for('verifySS', verifyS='verify_sb', verifySS='verify_ssb'))
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


@app.route('/verify/verifyS/<verifyS>/verifySS/<verifySS>',  methods=['GET'])
def verifySS(verifyS, verifySS):
    inputs = session['inputs']

    if verifySS == 'verify_ssa':
        proof_s = session['proof_sa']
    elif verifySS == 'verify_ssb':
        proof_s = session['proof_sb']

    E = proof_s['E']
    F = proof_s['F']
    proof = proofSS(proof_s['proof_c'], proof_s['proof_D'], proof_s['proof_D1'], proof_s['proof_D2'])

    val = {'E': E, 'F': F, 'g1': F, 'g2': inputs['g'], 'h1': inputs['h'], 'h2': inputs['h']}
    result, ext = verifySS_Flask(E, F, inputs['n'], F, inputs['g'], inputs['h'], inputs['h'], proof)

    return render_template('verify_ss.html', inputs=inputs, proof=proof, val=val, ext=ext, result=int(result))



@app.route('/prove/proveLI/<proveLI>', methods=['POST', 'GET'])
def proveLI(proveLI):
    if request.method == 'POST':
        if request.form['proveLI'] == 'verify':
            if proveLI == 'proof_lia':
                return redirect(url_for('verifyLI', verifyLI="verify_lia"))
            elif proveLI == 'proof_lib':
                return redirect(url_for('verifyLI', verifyLI="verify_lib"))
    else:
        inputs = session['inputs']
        ext_wt = session['ext_wt']
        params = session['params']

        if proveLI == 'proof_lia':
            proof = session['proof_lia']
            ext_li = session['ext_lia']
            ext = {'x': ext_wt['xa2'], 'r': ext_wt['ra2']}
        elif proveLI == 'proof_lib':
            proof = session['proof_lib']
            ext_li = session['ext_lib']
            ext = {'x': ext_wt['xb2'], 'r': ext_wt['rb2']}
        else:
            assert True, 'Prueba no encontrada'

        return render_template('prove_li.html', proof=proof, ext_li=ext_li, inputs=inputs, params=params, ext=ext)


@app.route('/verify/verifyLI/<verifyLI>', methods=['GET'])
def verifyLI(verifyLI):
    inputs = session['inputs']
    params = session['params']
    proof_wt = session['proof_wt']

    params_ = paramsLI(params['t'], params['l'], params['s'])

    if verifyLI == 'verify_lia':
        proof = session['proof_lia']
        proof_ = proofLI(proof['C'], proof['D1'], proof['D2'], proof['c'])
        E = proof_wt['Ea2']
    elif verifyLI == 'verify_lib':
        proof = session['proof_lib']
        proof_ = proofLI(proof['C'], proof['D1'], proof['D2'], proof['c'])
        E = proof_wt['Eb2']

    result, ext = verifyLI_Flask(E, inputs['n'], inputs['g'], inputs['h'], inputs['b'], proof_, params_)

    return render_template('verify_li.html', inputs=inputs, params=params, proof=proof, ext=ext, result=int(result))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
