import React from "react";
import {button_click__dataLayer, init_page__dataLayer} from "../module/dataLayer";
import {Mouse} from "../component/mouse";
import {Footer} from "../component/footer";

export class Home extends React.Component {

    constructor(props) {
        super(props);
        init_page__dataLayer("HOME");
        setTimeout(() => {
            this.animation_scroll();
        }, 200);
    }

    animation_scroll() {
        const nb_slide_total = 5
        let sliding_list = [];
        for (let nb_slide = 1; nb_slide <= nb_slide_total; nb_slide++) {
            sliding_list.push(document.querySelector('.slide' + nb_slide.toString()));
        }
        const multiplicative = 0.6;
        window.addEventListener('scroll', () => {
            const {scrollTop, clientHeight} = document.documentElement;
            let topElementToTopViewport = [];
            for (let nb_slide = 0; nb_slide < nb_slide_total; nb_slide++) {
                topElementToTopViewport.push(sliding_list[nb_slide].getBoundingClientRect().top);
            }

            for (let nb_slide = 0; nb_slide < nb_slide_total; nb_slide++) {
                if (scrollTop > (scrollTop + topElementToTopViewport[nb_slide]).toFixed() - clientHeight * multiplicative) {
                    sliding_list[nb_slide].classList.add('active' + (nb_slide + 1).toString());
                }
            }

        })
    }


    render() {
        return (<div>
            <Mouse/>
            <div class={"container-home container-home-page"}>
                <h1><img alt={"logo"}
                         src={"https://media.discordapp.net/attachments/1047568954845048944/1164928988586721390/logo_2.png?ex=6544ffaa&is=65328aaa&hm=a8778c1c34340bd698ddbf414541b04cc0fda897605e7f10dfa610404a05ce94&=&width=578&height=578"}/>
                </h1>
                <h2>Pour une baignade surveillée !</h2>
                <div class={"btn-download"} onClick={() => {
                    window.open("https://play.google.com/store/apps/details?id=com.anonymous.C2SMR");
                    button_click__dataLayer("download");
                }}>DOWNLOAD
                </div>
                <div class={"wrapper-img a"}>
                    <img alt={"img-round-pres"}
                         src={"https://media.discordapp.net/attachments/1084071570567335956/1162305243846029404/image.png?ex=653b741c&is=6528ff1c&hm=24addab4efaf096a3e58f0f711ba635368792dac576a7d4b80210921ad1f7695&=&width=1000&height=521"}/>
                </div>
                <div className={"wrapper-img b"}>
                    <img alt={"img-round-pres"}
                         src={"https://media.discordapp.net/attachments/1125864163391066186/1166836472427593728/image.png?ex=654bf025&is=65397b25&hm=93adbcfe4793897a0447b72bb6bb5d275eab244c3956f5c447ea258404d8a14f&=&width=1042&height=500"}/>
                </div>
                <div className={"wrapper-img c"}>
                    <img alt={"img-round-pres"}
                         src={"https://media.discordapp.net/attachments/1125864163391066186/1166836579403300894/image.png?ex=654bf03f&is=65397b3f&hm=0a648c352920d9e7f834f74aa5a701210972a1abb36b41b60f54d978fefaf600&=&width=1042&height=373"}/>
                </div>
            </div>
            <div class={"container-safe-beach container-home-page"}>
                <div className={"wrapper"}>
                    <h2>Retrouver toutes les informations en allant à la plage et aider à alerter.</h2>
                    <div className={"btn-download"} onClick={() => {
                        window.open("https://play.google.com/store/apps/details?id=com.anonymous.C2SMR");
                        button_click__dataLayer("download_page_2");
                    }}>DOWNLOAD
                    </div>
                </div>
                <img alt={"img app-pres 1"} class={"slide1"}
                     src={"https://media.discordapp.net/attachments/1084071570567335956/1166835513328672788/image.png?ex=654bef41&is=65397a41&hm=59b5ed2759595f8c5540cc46b16449ba8287303613bf5eb1fc17f09d8b8e19b5&"}/>
            </div>
            <div class={"container-roboflow container-home-page"}>
                <h2>Qui sommes-nous ?</h2>
                <h3><span>C2SMR</span> est une association à but non lucratif loi 1901 dont l’objectif est d'aider
                    le sauvetage marin à l'aide d'analyse d'image par ordinateur.</h3>
                <h3><span>Open source</span> : Tout notre code est disponible en accès libre et co-développé par nos
                    bénévoles.
                    Nous pensons que l'intelligence collective est la meilleure façon de résoudre un problème
                    complexe.</h3>
                <h3><span>Détection précoce </span>: Pour lutter efficacement contre les noyades il est important de
                    les
                    détecter de façon précoce pour permettre une intervention rapide des
                    secours. </h3>
                <h3>Retrouvez notre dataset sur <span class={"link"} onClick={() => {
                    window.open("https://universe.roboflow.com/c2smr");
                    button_click__dataLayer("roboflow");
                }}>ROBOFLOW</span> et notre code sur <span className={"link"} onClick={() => {
                    window.open("https://github.com/C2SMR");
                    button_click__dataLayer("github");
                }}>GITHUB</span> .</h3>
            </div>
            <div class={"container-types-sensors container-home-page"}>
                <div class={"cam"}>
                    <img alt={"camera"}
                         class={"slide5"}
                         src={"https://media.discordapp.net/attachments/1084071570567335956/1162300945821085716/d8218.png?ex=653b701b&is=6528fb1b&hm=981f90f867afbc221e10e24b7be71c8a5c8162237a31f5dd0cd0fca9b079e7d4&=&width=578&height=578"}/>
                    <h3>Installation manuelle !</h3>
                </div>
                <div class={"yt"}>
                    <img alt={"yt"} class={"slide2"}
                         src={"https://media.discordapp.net/attachments/1084071570567335956/1162301584600993812/image.png?ex=653b70b4&is=6528fbb4&hm=71a35be1a4f23727df04970b4e48fcfa3eb9f27484d714ed500e017179cc101b&=&width=883&height=578"}/>
                    <h3>Via une webcam Public !</h3>
                </div>
            </div>
            <div class={"container-join container-home-page"}>
                <h2 class={"slide3"}>Comment le mettre en place ?</h2>
                <div class={"btn-join slide4"} onClick={() => {
                    window.location.href = "mailto:victordalet@protonmail.com"
                    button_click__dataLayer("join");
                }}>Nous contacter
                </div>
            </div>
            <Footer/>
        </div>);
    }
}
