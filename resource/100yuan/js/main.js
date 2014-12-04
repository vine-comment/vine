H = 1E3;
var qp_a = W / 4,
    qp_b = H / 4,
    qp_c = 3,
    qp_d = 0,
    qp_e = 0,
    qp_f, qp_g, qp_h, qp_i, qp_j = 15,
    qp_k = 32,
    qp_l = 150,
    qp_m, qp_n = 0,
    qp_o = 0,
    qp_p, qp_q = ["jihijjjiiijlljihijjjjiijihjihijjjiiijlljihijjjjiijih",
         "jjkllkjihhijjiijjkllkjihhijihhiijhijkjhijkjhhiljjkllkjihhijihh",
         "hhllmmlkkjjiihllkkjjillkkjjihhllmmlkkjjiih"];

function qp_r() {
    qp_o >= qp_q[qp_n].length && (qp_o = 0, qp_n = qp_s(qp_q.length));
    return qp_q[qp_n][qp_o++]
}

function qp_t(a) {
    IS_ANDROID &&
     (createjs.Sound.registMySound("h", 0),
      createjs.Sound.registMySound("i", 2),
      createjs.Sound.registMySound("j", 4), 
      createjs.Sound.registMySound("k", 6), 
      createjs.Sound.registMySound("l", 8), 
      createjs.Sound.registMySound("m", 10), 
      createjs.Sound.registMySound("n", 12), 
      createjs.Sound.registMySound("silenttail", 14));

    qp_u();
    qipaStage.stage.player = new Qp_v;
    qipaStage.stage.addChild(qipaStage.stage.player);
    qipaStage.stage.gameoverlayer = new Qp_w;
    qipaStage.stage.gameoverlayer.visible = !1;
    qipaStage.stage.addChild(qipaStage.stage.gameoverlayer);
    qipaApp.onGameStarted();
    qp_x()
}

function qp_u() {
    qipaStage.stage.background = new createjs.Shape;
    qipaStage.stage.background.graphics.beginFill("white").rect(0, 0, W, H);
    qipaStage.stage.addChild(qipaStage.stage.background);
    qipaStage.stage.background.on("mousedown", function(a) {
        IS_TOUCH && a.nativeEvent instanceof MouseEvent || qp_y(a.localX, a.localY)
    })
}

function Qp_w() {
    this.initialize();
    this.background = new createjs.Shape;
    this.background.graphics.beginFill("black").drawRect(0, 0, W, H);
    this.addChild(this.background);
    this.scoreText = new createjs.Text("得分：" + qipaApp.score, "bold 48px Arial", "white");
    this.scoreText.x = 225;
    this.scoreText.y = 230;
    this.addChild(this.scoreText);
    this.bestText = new createjs.Text("最高成绩: " + qipaApp.best, "bold 48px Arial", "white");
    this.bestText.x = 150;
    this.bestText.y = 380;
    this.addChild(this.bestText);
    this.bt_regame =
        new createjs.Text("重玩", "bold 48px Arial", "white");
    this.bt_regame.x = 80;
    ENABLE_LB || ENABLE_SHARE || (this.bt_regame.x = 300);
    this.bt_regame.y = 650;
    var a;
    a = new createjs.Shape;
    a.graphics.beginFill("black").rect(0, 0, 150, 50);
    this.bt_regame.hitArea = a;
    this.bt_regame.on("click", function(a) {
        IS_TOUCH && a.nativeEvent instanceof MouseEvent || qp_z()
    });
    this.addChild(this.bt_regame);

    ENABLE_SHARE && (this.bt_share = new createjs.Text("分享", "bold 48px Arial", "white"), this.bt_share.x = 440, this.bt_share.y = 650,
        a = new createjs.Shape, a.graphics.beginFill("black").rect(0, 0, 150, 50), this.bt_share.hitArea = a, this.bt_share.on("click", function(a) {
            IS_TOUCH && a.nativeEvent instanceof MouseEvent || qipaStage.showShareTip()
        }), this.addChild(this.bt_share));

    ENABLE_LB && (this.bt_top = new createjs.Text("排行榜", "bold 48px Arial", "white"),
                    this.bt_top.x = 240, this.bt_top.y = 650,
                    a = new createjs.Shape,
                    a.graphics.beginFill("black").rect(0, 0, 150, 50),
                    this.bt_top.hitArea = a,
                    this.bt_top.on("click", function(a) {
                        IS_TOUCH && a.nativeEvent instanceof
                        MouseEvent || window.open("../lb.html?gid=" + GID)
    }), this.addChild(this.bt_top))
}
Qp_w.prototype = new createjs.Container;

function qp_A(a) {
    "*" == a ? createjs.Sound.play("over", !0) : createjs.Sound.play(a, !0)
}

function qp_z() {
    qipaStage.stage.player.reset();
    qipaStage.stage.player.visible = !0;
    qipaStage.stage.background.visible = !0;
    qipaStage.stage.gameoverlayer.visible = !1;
    qipaApp.onGameStarted()
}

function qp_B() {
    qipaStage.stage.gameoverlayer.pushScore();
    qipaStage.stage.player.visible = !1;
    qipaStage.stage.background.visible = !1;
    qipaStage.stage.gameoverlayer.visible = !0;
    qp_m.visible = !1
}

function qp_C() {
    createjs.Ticker.removeEventListener("tick", qp_D);
    qipaApp.onNewScore(qipaApp.score);
    setTimeout("qp_B()", 150);
    qipaApp.onGameOver();
    qp_x()
}
Qp_w.prototype.pushScore = function() {
    this.scoreText.text = "得分: " + qipaApp.score;
    this.bestText.text = qipaApp.score > qipaApp.best ? "最高得分: " + qipaApp.score : "最高得分: " + qipaApp.best
};

function qp_E(a) {
    qipaApp.score += 1;
    qipaStage.stage.player.scoreText.text = qipaApp.score;
    qp_A(qp_r());
    qp_i[a].x = qp_f[qp_c].x;
    qp_i[a].y = qp_f[qp_c].y;
    qp_i[a].inUse = !0;
    qp_i[a].visible = !0;
    qp_f[qp_c].clicked = !0;
    qp_F()
}

function qp_y(a, b) {
    var c = qp_f[qp_c];
    qp_G(a, b) ? !0 == qp_p.visible ? (qp_p.visible = !1, qp_E(qp_H()), createjs.Ticker.addEventListener("tick", qp_D)) : qp_E(qp_H()) : b > c.y && b < c.y + qp_b && (qp_m.x = parseInt(parseInt(a) / qp_a) * qp_a, qp_m.y = c.y, qp_m.visible = !0, qp_A("*"), qp_C())
}

function qp_H() {
    var a;
    for (a = 0; a < qp_i.length; a++)
        if (!1 == qp_i[a].inUse) return a
}

function qp_G(a, b) {
    var c = qp_f[qp_c],
        d = c.y - qp_b,
        e = c.y + 2 * qp_b > H ? H : c.y + 2 * qp_b;
    return a > c.x && a < c.x + qp_a && b > d && b < e ? !0 : !1
}

function qp_F() {
    qp_c--;
    0 > qp_c && (qp_c = 4)
}

function qp_s(a) {
    return parseInt(100 * Math.random()) % a
}

function Qp_v() {
    this.initialize();
    this.genObjects()
}
Qp_v.prototype = new createjs.Container;
Qp_v.prototype.genObjects = function() {
    var a;
    qp_f = [];
    for (var b = 0; 5 > b; b++)
        a = new createjs.Shape,
        a.graphics.beginFill("black").rect(0, 0, qp_a, qp_b),
        a.x = qp_s(4) * qp_a, a.y = qp_b * (b - 1),
        a.clicked = 4 == b ? !0 : !1,
        this.addChild(a),
        3 == b && (qp_p = new createjs.Text("开始", "bold 60px Arial", "white"), qp_p.x = a.x + 20, qp_p.y = a.y + 90, this.addChild(qp_p)), qp_f.push(a);
    qp_m = new createjs.Shape;
    qp_m.graphics.beginFill("red").rect(0, 0, qp_a, qp_b);
    qp_m.visible = !1;
    this.addChild(qp_m);
    qp_h = new createjs.Shape;
    qp_h.graphics.beginFill("yellow").rect(0,
        0, W, qp_b);
    qp_h.y = 3 * qp_b;
    this.addChild(qp_h);
    qp_i = [];
    for (a = 0; 5 > a; a++) b = new createjs.Shape, b.graphics.beginFill("grey").rect(0, 0, qp_a, qp_b), b.visible = !1, b.inUse = !1, this.addChild(b), qp_i.push(b);
    qp_g = [];
    for (b = 0; 5 > b; b++) a = new createjs.Shape, a.graphics.setStrokeStyle(1, "round").beginStroke("black").moveTo(b * qp_a, 0).lineTo(b * qp_a, H), this.addChild(a);
    for (b = 0; 6 > b; b++) a = new createjs.Shape, a.graphics.setStrokeStyle(1.5, "round").beginStroke("black").moveTo(0, (b - 1) * qp_b).lineTo(W, (b - 1) * qp_b), this.addChild(a),
        qp_g.push(a);
    this.scoreText = new createjs.Text("0", "bold 48px Arial", "red");
    this.scoreText.x = W / 2;
    this.scoreText.y = 50;
    this.addChild(this.scoreText)
};
Qp_v.prototype.reset = function() {
    qp_o = qipaApp.score = 0;
    qp_c = 3;
    qp_n = qp_s(qp_q.length);
    qp_d = 0;
    for (var a, b = 0; b < qp_f.length; b++) a = qp_f[b], a.x = qp_s(4) * qp_a, a.y = qp_b * (b - 1), a.clicked = 4 == b ? !0 : !1, 3 == b && (qp_p.x = a.x + 20, qp_p.y = a.y + 90, qp_p.visible = !0);
    for (b = 0; b < qp_i.length; b++) qp_i[b].inUse = !1, qp_i[b].visible = !1;
    qp_h.y = 3 * qp_b;
    qp_h.visible = !0;
    for (b = 0; b < qp_g.length; b++) qp_g[b].y = 0;
    this.scoreText.text = qipaApp.score
};

function qp_I() {
    return qipaApp.score * (qp_k - qp_j) / (qipaApp.score + qp_l) + qp_j
}

function qp_D(a) {
    var b = qp_I();
    0 == qp_d ? (qp_d = a.timeStamp, qp_e = b) : (qp_e = (a.timeStamp - qp_d) * b / 20, qp_d = a.timeStamp);
    for (a = 0; a < qp_f.length; a++) b = qp_f[a], b.y + qp_e > H ? !1 == b.clicked ? (qp_C(), b.y = -H / 4 + qp_e + b.y - H, b.x = qp_s(4) * qp_a) : (b.y = -H / 4 + qp_e + b.y - H, b.x = qp_s(4) * qp_a, b.clicked = !1) : b.y += qp_e;
    for (a = 0; a < qp_i.length; a++) b = qp_i[a], b.y + qp_e > H ? (b.y = -H / 4 + qp_e + b.y - H, b.inUse = !1, b.visible = !1) : b.y += qp_e;
    for (a = 0; a < qp_g.length; a++) b = qp_g[a], b.y = b.y + qp_e > H ? -H / 2 + qp_e + b.y - H : b.y + qp_e;
    !0 == qp_h.visible && (qp_h.y + qp_e >= H ? qp_h.visible = !1 : qp_h.y += qp_e)
}

function qp_x() {
    qipaShare.title = "别踩白块儿（钢琴块）";
    if (0 == qipaApp.score) qipaShare.desc = qipaShare.title;
    else {
        var a = parseInt(Math.sqrt(1E4 * qipaApp.score / 300));
        99 < a && (a = "99.9");
        qipaShare.desc = "别踩白块儿：我得了" + qipaApp.score + "分，战胜了" + a + "%的玩家。不服来战！"
    }
}
var _cfg = {
    startFunc: qp_t,
    audio: {
        path: "audio/",
        manifest: [{
            src: "Acoustic_Grand_Piano_01.mp3",
            id: "h"
        }, {
            src: "Acoustic_Grand_Piano_02.mp3",
            id: "i"
        }, {
            src: "Acoustic_Grand_Piano_03.mp3",
            id: "j"
        }, {
            src: "Acoustic_Grand_Piano_04.mp3",
            id: "k"
        }, {
            src: "Acoustic_Grand_Piano_05.mp3",
            id: "l"
        }, {
            src: "Acoustic_Grand_Piano_06.mp3",
            id: "m"
        }, {
            src: "Acoustic_Grand_Piano_07.mp3",
            id: "n"
        }, {
            src: "false.mp3",
            id: "over"
        }]
    }
};
qipaStage.init(_cfg);