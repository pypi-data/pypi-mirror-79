let u=o=>o,x;import"../../web_modules/tippyjs/dist/tippy.css.proxy.js";import"../../web_modules/tippyjs/animations/shift-away-subtle.css.proxy.js";import"../../web_modules/react-toastify/dist/ReactToastify.css.proxy.js";import*as l from"../../web_modules/polished.js";import{createGlobalStyle as f,keyframes as g}from"../../web_modules/styled-components.js";import{css as y}from"../../web_modules/styled-components.js";export*from"../../web_modules/styled-components.js";export*from"../../web_modules/polished.js";export{borderRadius as borderRadiusShortHand,borderColor as borderColorShortHand,fontFace as fontFaceShortHand}from"../../web_modules/polished.js";const{math:m,size:c,lighten:a,darken:i,normalize:F,transitions:C,border:$,position:d}=l,b="14px";export const rem=o=>l.rem(o,b),em=(o,r)=>l.em(o,r||b),half=o=>m(`(${o}) / 2`),headerHeight=rem(60),contentMargin=rem(20),contentHeight=`calc(100vh - ${m(`${contentMargin} * 2 + ${headerHeight}`)})`,asideWidth=rem(260),borderRadius="4px",progressSpinnerSize="20px",primaryColor="#2932E1",dangerColor="#FF3912",primaryFocusedColor=a(.08,primaryColor),primaryActiveColor=a(.12,primaryColor),dangerFocusedColor=a(.08,dangerColor),dangerActiveColor=a(.12,dangerColor),selectedColor="#1A73E8",lightColor="#F4F5FC",lightFocusedColor=i(.03,lightColor),lightActiveColor=i(.06,lightColor),textColor="#333",textLightColor="#666",textLighterColor="#999",textInvertColor="#FFF",bodyBackgroundColor="#F4F4F4",primaryBackgroundColor="#F2F6FF",backgroundColor="#FFF",backgroundFocusedColor="#F6F6F6",borderColor="#DDD",borderFocusedColor=i(.15,borderColor),borderActiveColor=i(.3,borderColor),navbarBackgroundColor="#1527C2",navbarHoverBackgroundColor=a(.05,navbarBackgroundColor),navbarHighlightColor="#596cd6",progressBarColor="#FFF",maskColor="rgba(255, 255, 255, 0.8)",tooltipBackgroundColor="rgba(0, 0, 0, 0.6)",tooltipTextColor="#FFF",duration="75ms",easing="ease-in",sameBorder=(o="1px",r="solid",s=borderColor,t)=>{if(typeof o=="object"){var e,n,p;r=(e=o.type)!==null&&e!==void 0?e:"solid",s=(n=o.color)!==null&&n!==void 0?n:borderColor,t=o.radius===!0?borderRadius:o.radius,o=(p=o.width)!==null&&p!==void 0?p:"1px"}return Object.assign({},$(o,r,s),t?{borderRadius:t===!0?borderRadius:t}:void 0)},transitionProps=(o,r)=>{if(typeof o=="string"&&(o=[o]),typeof r!="string"){var s,t,e,n;r=`${(s=(t=r)===null||t===void 0?void 0:t.duration)!==null&&s!==void 0?s:duration} ${(e=(n=r)===null||n===void 0?void 0:n.easing)!==null&&e!==void 0?e:easing}`}return C(o,r)},link=y(["a{color:",";cursor:pointer;",";&:hover{color:",";}&:active{color:",";}}"],primaryColor,transitionProps("color"),primaryFocusedColor,primaryActiveColor);const h=g(["0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}"]);export const GlobalStyle=f(x||(x=u`
    ${0}

    html {
        font-size: ${0};
        font-family: 'Merriweather Sans', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    html,
    body {
        height: 100%;
        background-color: ${0};
        color: ${0};
    }

    a {
        text-decoration: none;
        color: inherit;

        &:visited {
            color: currentColor;
        }
    }

    * {
        box-sizing: border-box;
    }

    #nprogress {
        pointer-events: none;
    }

    #nprogress .bar {
        background: ${0};
        z-index: 99999;
        ${0}
        ${0}
    }

    #nprogress .peg {
        display: block;
        ${0}
        ${0}
        box-shadow: 0 0 rem(10) ${0}, 0 0 ${0} ${0};
        opacity: 1;
        transform: rotate(3deg) translate(0px, -${0});
    }

    #nprogress .spinner {
        display: block;
        z-index: 99999;
        ${0}
    }

    #nprogress .spinner-icon {
        ${0}
        box-sizing: border-box;

        border: solid 2px transparent;
        border-top-color: ${0};
        border-left-color: ${0};
        border-radius: 50%;

        animation: ${0} 400ms linear infinite;
    }

    .nprogress-custom-parent {
        overflow: hidden;
        position: relative;
    }

    .nprogress-custom-parent #nprogress .spinner,
    .nprogress-custom-parent #nprogress .bar {
        position: absolute;
    }

    .Toastify__toast-container {
        z-index: 10001;

        .Toastify__toast {
            border-radius: ${0};
        }

        .Toastify__toast--default {
            color: ${0};
        }

        .Toastify__toast-body {
            padding: 0 1.428571429em;
        }
    }

    [data-tippy-root] .tippy-box {
        z-index: 10002;
        color: ${0};
        background-color: ${0};
        box-shadow: 0 0 10px 0 rgba(0,0,0,0.10);
        border-radius: ${0};

        > .tippy-content {
            padding: 0;
            /* trigger bfc */
            display: flow-root;
        }

        &[data-placement^='top'] > .tippy-arrow::before {
            border-top-color: ${0};
        }
        &[data-placement^='bottom'] > .tippy-arrow::before {
            border-bottom-color: ${0};
        }
        &[data-placement^='left'] > .tippy-arrow::before {
            border-left-color: ${0};
        }
        &[data-placement^='right'] > .tippy-arrow::before {
            border-right-color: ${0};
        }

        &[data-theme~='tooltip'] {
            color: ${0};
            background-color: ${0};
            box-shadow: none;

            > .tippy-content {
                padding: ${0} ${0};
            }

            &[data-placement^='top'] > .tippy-arrow::before {
                border-top-color: ${0};
            }
            &[data-placement^='bottom'] > .tippy-arrow::before {
                border-bottom-color: ${0};
            }
            &[data-placement^='left'] > .tippy-arrow::before {
                border-left-color: ${0};
            }
            &[data-placement^='right'] > .tippy-arrow::before {
                border-right-color: ${0};
            }
        }
    }
`),F,b,bodyBackgroundColor,textColor,progressBarColor,d("fixed",0,null,null,0),c("2px","100%"),d("absolute",null,0,null,null),c("100%",rem(100)),progressBarColor,rem(5),progressBarColor,rem(4),d("fixed",progressSpinnerSize,progressSpinnerSize,null,null),c(`calc(${half(headerHeight)} - ${half(progressSpinnerSize)})`),progressBarColor,progressBarColor,h,borderRadius,textColor,textColor,backgroundColor,borderRadius,backgroundColor,backgroundColor,backgroundColor,backgroundColor,tooltipTextColor,tooltipBackgroundColor,rem(5),rem(9),tooltipBackgroundColor,tooltipBackgroundColor,tooltipBackgroundColor,tooltipBackgroundColor);
