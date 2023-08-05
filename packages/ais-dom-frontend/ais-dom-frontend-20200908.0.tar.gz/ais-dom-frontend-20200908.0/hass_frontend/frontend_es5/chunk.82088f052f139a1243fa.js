/*! For license information please see chunk.82088f052f139a1243fa.js.LICENSE.txt */
(self.webpackJsonp=self.webpackJsonp||[]).push([[70],{172:function(t,e,n){"use strict";n(5);var i={properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(t,e){for(var n in e)t[n]=e[n]},_cloneConfig:function(t){var e={isClone:!0};return this._copyProperties(e,t),e},_getAnimationConfigRecursive:function(t,e,n){var i;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(i=t?this.animationConfig[t]:this.animationConfig,Array.isArray(i)||(i=[i]),i)for(var o,r=0;o=i[r];r++)if(o.animatable)o.animatable._getAnimationConfigRecursive(o.type||t,e,n);else if(o.id){var a=e[o.id];a?(a.isClone||(e[o.id]=this._cloneConfig(a),a=e[o.id]),this._copyProperties(a,o)):e[o.id]=o}else n.push(o)},getAnimationConfig:function(t){var e={},n=[];for(var i in this._getAnimationConfigRecursive(t,e,n),e)n.push(e[i]);return n}};n.d(e,"a",(function(){return o}));var o=[i,{_configureAnimations:function(t){var e=[],n=[];if(t.length>0)for(var i,o=0;i=t[o];o++){var r=document.createElement(i.name);if(r.isNeonAnimation){var a;r.configure||(r.configure=function(t){return null}),a=r.configure(i),n.push({result:a,config:i,neonAnimation:r})}else console.warn(this.is+":",i.name,"not found!")}for(var s=0;s<n.length;s++){var l=n[s].result,c=n[s].config,u=n[s].neonAnimation;try{"function"!=typeof l.cancel&&(l=document.timeline.play(l))}catch(d){l=null,console.warn("Couldnt play","(",c.name,").",d)}l&&e.push({neonAnimation:u,config:c,animation:l})}return e},_shouldComplete:function(t){for(var e=!0,n=0;n<t.length;n++)if("finished"!=t[n].animation.playState){e=!1;break}return e},_complete:function(t){for(var e=0;e<t.length;e++)t[e].neonAnimation.complete(t[e].config);for(e=0;e<t.length;e++)t[e].animation.cancel()},playAnimation:function(t,e){var n=this.getAnimationConfig(t);if(n){this._active=this._active||{},this._active[t]&&(this._complete(this._active[t]),delete this._active[t]);var i=this._configureAnimations(n);if(0!=i.length){this._active[t]=i;for(var o=0;o<i.length;o++)i[o].animation.onfinish=function(){this._shouldComplete(i)&&(this._complete(i),delete this._active[t],this.fire("neon-animation-finish",e,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",e,{bubbles:!1})}},cancelAnimation:function(){for(var t in this._active){var e=this._active[t];for(var n in e)e[n].animation.cancel()}this._active={}}}]},247:function(t,e,n){"use strict";n.d(e,"b",(function(){return r})),n.d(e,"a",(function(){return a}));n(5);var i=n(119),o=n(3),r={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(t,e){e&&(t?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(t){this.closingReason=this.closingReason||{},this.closingReason.confirmed=t},_onDialogClick:function(t){for(var e=Object(o.a)(t).path,n=0,i=e.indexOf(this);n<i;n++){var r=e[n];if(r.hasAttribute&&(r.hasAttribute("dialog-dismiss")||r.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(r.hasAttribute("dialog-confirm")),this.close(),t.stopPropagation();break}}}},a=[i.a,r]},278:function(t,e,n){"use strict";n(5),n(47),n(52),n(57),n(118);var i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(i.content);var o=n(172),r=n(247),a=n(6),s=n(4);function l(){var t=function(t,e){e||(e=t.slice(0));return Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(e)}}))}(['\n    <style include="paper-dialog-shared-styles"></style>\n    <slot></slot>\n']);return l=function(){return t},t}Object(a.a)({_template:Object(s.a)(l()),is:"paper-dialog",behaviors:[r.a,o.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},284:function(t,e,n){"use strict";n(278);var i=n(92),o=n(175),r=n(3),a={getTabbableNodes:function(t){var e=[];return this._collectTabbableNodes(t,e)?o.a._sortByTabIndex(e):e},_collectTabbableNodes:function(t,e){if(t.nodeType!==Node.ELEMENT_NODE||!o.a._isVisible(t))return!1;var n,i=t,a=o.a._normalizedTabIndex(i),s=a>0;a>=0&&e.push(i),n="content"===i.localName||"slot"===i.localName?Object(r.a)(i).getDistributedNodes():Object(r.a)(i.shadowRoot||i.root||i).children;for(var l=0;l<n.length;l++)s=this._collectTabbableNodes(n[l],e)||s;return s}};function s(t){return(s="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function l(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function c(t,e){return(c=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t})(t,e)}function u(t,e){return!e||"object"!==s(e)&&"function"!=typeof e?function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t):e}function d(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(t){return!1}}function p(t){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}var h=customElements.get("paper-dialog"),f={get _focusableNodes(){return a.getTabbableNodes(this)}},m=function(t){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&c(t,e)}(i,t);var e,n=(e=i,function(){var t,n=p(e);if(d()){var i=p(this).constructor;t=Reflect.construct(n,arguments,i)}else t=n.apply(this,arguments);return u(this,t)});function i(){return l(this,i),n.apply(this,arguments)}return i}(Object(i.b)([f],h));customElements.define("ha-paper-dialog",m)},293:function(t,e,n){"use strict";n(5),n(47),n(52);var i=n(247),o=n(6),r=n(4);function a(){var t=function(t,e){e||(e=t.slice(0));return Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(e)}}))}(['\n    <style>\n\n      :host {\n        display: block;\n        @apply --layout-relative;\n      }\n\n      :host(.is-scrolled:not(:first-child))::before {\n        content: \'\';\n        position: absolute;\n        top: 0;\n        left: 0;\n        right: 0;\n        height: 1px;\n        background: var(--divider-color);\n      }\n\n      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {\n        content: \'\';\n        position: absolute;\n        bottom: 0;\n        left: 0;\n        right: 0;\n        height: 1px;\n        background: var(--divider-color);\n      }\n\n      .scrollable {\n        padding: 0 24px;\n\n        @apply --layout-scroll;\n        @apply --paper-dialog-scrollable;\n      }\n\n      .fit {\n        @apply --layout-fit;\n      }\n    </style>\n\n    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">\n      <slot></slot>\n    </div>\n']);return a=function(){return t},t}Object(o.a)({_template:Object(r.a)(a()),is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(i.b)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},589:function(t,e,n){"use strict";n.r(e);n(293),n(188),n(76);var i=n(0),o=n(49),r=n(11),a=window.SpeechRecognition||window.webkitSpeechRecognition;window.SpeechGrammarList||window.webkitSpeechGrammarList,window.SpeechRecognitionEvent||window.webkitSpeechRecognitionEvent;function s(){return Math.floor(65536*(1+Math.random())).toString(16).substring(1)}n(284);var l=function(t,e,n){return t.callWS({type:"conversation/process",text:e,conversation_id:n})},c=n(55);function u(t){return(u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function d(){var t=_(['\n        :host {\n          z-index: 103;\n        }\n\n        ha-icon-button {\n          color: var(--secondary-text-color);\n        }\n\n        ha-icon-button[active] {\n          color: var(--primary-color);\n        }\n\n        .input {\n          margin: 0 0 16px 0;\n        }\n\n        ha-paper-dialog {\n          width: 450px;\n        }\n        a.button {\n          text-decoration: none;\n        }\n        a.button > mwc-button {\n          width: 100%;\n        }\n        .onboarding {\n          padding: 0 24px;\n        }\n        paper-dialog-scrollable.top-border::before {\n          content: "";\n          position: absolute;\n          top: 0;\n          left: 0;\n          right: 0;\n          height: 1px;\n          background: var(--divider-color);\n        }\n        .side-by-side {\n          display: flex;\n          margin: 8px 0;\n        }\n        .side-by-side > * {\n          flex: 1 0;\n          padding: 4px;\n        }\n        .attribution {\n          color: var(--secondary-text-color);\n        }\n        .message {\n          font-size: 18px;\n          clear: both;\n          margin: 8px 0;\n          padding: 8px;\n          border-radius: 15px;\n        }\n\n        .message.user {\n          margin-left: 24px;\n          float: right;\n          text-align: right;\n          border-bottom-right-radius: 0px;\n          background-color: var(--light-primary-color);\n          color: var(--text-light-primary-color, var(--primary-text-color));\n        }\n\n        .message.hass {\n          margin-right: 24px;\n          float: left;\n          border-bottom-left-radius: 0px;\n          background-color: var(--primary-color);\n          color: var(--text-primary-color);\n        }\n\n        .message a {\n          color: var(--text-primary-color);\n        }\n\n        .message img {\n          width: 100%;\n          border-radius: 10px;\n        }\n\n        .message.error {\n          background-color: var(--error-color);\n          color: var(--text-primary-color);\n        }\n\n        .interimTranscript {\n          color: var(--secondary-text-color);\n        }\n\n        .bouncer {\n          width: 48px;\n          height: 48px;\n          position: absolute;\n          top: 0;\n        }\n        .double-bounce1,\n        .double-bounce2 {\n          width: 48px;\n          height: 48px;\n          border-radius: 50%;\n          background-color: var(--primary-color);\n          opacity: 0.2;\n          position: absolute;\n          top: 0;\n          left: 0;\n          -webkit-animation: sk-bounce 2s infinite ease-in-out;\n          animation: sk-bounce 2s infinite ease-in-out;\n        }\n        .double-bounce2 {\n          -webkit-animation-delay: -1s;\n          animation-delay: -1s;\n        }\n        @-webkit-keyframes sk-bounce {\n          0%,\n          100% {\n            -webkit-transform: scale(0);\n          }\n          50% {\n            -webkit-transform: scale(1);\n          }\n        }\n        @keyframes sk-bounce {\n          0%,\n          100% {\n            transform: scale(0);\n            -webkit-transform: scale(0);\n          }\n          50% {\n            transform: scale(1);\n            -webkit-transform: scale(1);\n          }\n        }\n\n        @media all and (max-width: 450px), all and (max-height: 500px) {\n          .message {\n            font-size: 16px;\n          }\n        }\n      ']);return d=function(){return t},t}function p(t){return function(t){if(Array.isArray(t))return I(t)}(t)||N(t)||z(t)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function h(){var t=_(["\n                <a\n                  href=",'\n                  class="attribution"\n                  target="_blank"\n                  rel="noreferrer"\n                  >',"</a\n                >\n              "]);return h=function(){return t},t}function f(){var t=_(['\n                          <div class="bouncer">\n                            <div class="double-bounce1"></div>\n                            <div class="double-bounce2"></div>\n                          </div>\n                        ']);return f=function(){return t},t}function m(){var t=_(['\n                  <span suffix="" slot="suffix">\n                    ','\n                    <ha-icon-button\n                      icon="hass:microphone"\n                      @click=',"\n                    >\n                    </ha-icon-button>\n                  </span>\n                "]);return m=function(){return t},t}function g(){var t=_(['\n                <div class="message user">\n                  <span\n                    class=',"\n                    >","</span\n                  >","\n                </div>\n              "]);return g=function(){return t},t}function b(){var t=_(['\n              <div class="','">\n                ',"\n              </div>\n            "]);return b=function(){return t},t}function v(){var t=_(['\n              <div class="onboarding">\n                ','\n                <div class="side-by-side" @click=','>\n                  <a\n                    class="button"\n                    href="','"\n                    target="_blank"\n                    rel="noreferrer"\n                    ><mwc-button unelevated>Yes!</mwc-button></a\n                  >\n                  <mwc-button outlined>No</mwc-button>\n                </div>\n              </div>\n            ']);return v=function(){return t},t}function y(){var t=_(["\n      <style>\n        paper-dialog-scrollable {\n          --paper-dialog-scrollable: {\n            -webkit-overflow-scrolling: auto;\n            max-height: 50vh !important;\n          }\n        }\n\n        paper-dialog-scrollable.can-scroll {\n          --paper-dialog-scrollable: {\n            -webkit-overflow-scrolling: touch;\n            max-height: 50vh !important;\n          }\n        }\n\n        @media all and (max-width: 450px), all and (max-height: 500px) {\n          paper-dialog-scrollable {\n            --paper-dialog-scrollable: {\n              -webkit-overflow-scrolling: auto;\n              max-height: calc(100vh - 175px) !important;\n            }\n          }\n\n          paper-dialog-scrollable.can-scroll {\n            --paper-dialog-scrollable: {\n              -webkit-overflow-scrolling: touch;\n              max-height: calc(75vh - 175px) !important;\n            }\n          }\n        }\n      </style>\n      <ha-paper-dialog\n        with-backdrop\n        .opened=","\n        @opened-changed=","\n      >\n        ",'\n        <paper-dialog-scrollable\n          id="messages"\n          class=',"\n        >\n          ","\n          ",'\n        </paper-dialog-scrollable>\n        <div class="input">\n          <paper-input\n            @keyup=','\n            label="','"\n            autofocus\n          >\n            ',"\n          </paper-input>\n          ","\n        </div>\n      </ha-paper-dialog>\n    "]);return y=function(){return t},t}function _(t,e){return e||(e=t.slice(0)),Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(e)}}))}function k(t,e,n,i,o,r,a){try{var s=t[r](a),l=s.value}catch(c){return void n(c)}s.done?e(l):Promise.resolve(l).then(i,o)}function w(t){return function(){var e=this,n=arguments;return new Promise((function(i,o){var r=t.apply(e,n);function a(t){k(r,i,o,a,s,"next",t)}function s(t){k(r,i,o,a,s,"throw",t)}a(void 0)}))}}function x(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function O(t,e){return(O=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t})(t,e)}function C(t,e){return!e||"object"!==u(e)&&"function"!=typeof e?E(t):e}function E(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}function j(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(t){return!1}}function A(t){var e,n=D(t.key);"method"===t.kind?e={value:t.value,writable:!0,configurable:!0,enumerable:!1}:"get"===t.kind?e={get:t.value,configurable:!0,enumerable:!1}:"set"===t.kind?e={set:t.value,configurable:!0,enumerable:!1}:"field"===t.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===t.kind?"field":"method",key:n,placement:t.static?"static":"field"===t.kind?"own":"prototype",descriptor:e};return t.decorators&&(i.decorators=t.decorators),"field"===t.kind&&(i.initializer=t.value),i}function T(t,e){void 0!==t.descriptor.get?e.descriptor.get=t.descriptor.get:e.descriptor.set=t.descriptor.set}function S(t){return t.decorators&&t.decorators.length}function P(t){return void 0!==t&&!(void 0===t.value&&void 0===t.writable)}function R(t,e){var n=t[e];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+e+"' to be a function");return n}function D(t){var e=function(t,e){if("object"!==u(t)||null===t)return t;var n=t[Symbol.toPrimitive];if(void 0!==n){var i=n.call(t,e||"default");if("object"!==u(i))return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(t)}(t,"string");return"symbol"===u(e)?e:String(e)}function z(t,e){if(t){if("string"==typeof t)return I(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);return"Object"===n&&t.constructor&&(n=t.constructor.name),"Map"===n||"Set"===n?Array.from(n):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?I(t,e):void 0}}function I(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,i=new Array(e);n<e;n++)i[n]=t[n];return i}function N(t){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(t))return Array.from(t)}function B(t,e,n){return(B="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,e,n){var i=function(t,e){for(;!Object.prototype.hasOwnProperty.call(t,e)&&null!==(t=M(t)););return t}(t,e);if(i){var o=Object.getOwnPropertyDescriptor(i,e);return o.get?o.get.call(n):o.value}})(t,e,n||t)}function M(t){return(M=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}n.d(e,"HaVoiceCommandDialog",(function(){return L}));var L=function(t,e,n,i){var o=function(){(function(){return t});var t={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(t,e){["method","field"].forEach((function(n){e.forEach((function(e){e.kind===n&&"own"===e.placement&&this.defineClassElement(t,e)}),this)}),this)},initializeClassElements:function(t,e){var n=t.prototype;["method","field"].forEach((function(i){e.forEach((function(e){var o=e.placement;if(e.kind===i&&("static"===o||"prototype"===o)){var r="static"===o?t:n;this.defineClassElement(r,e)}}),this)}),this)},defineClassElement:function(t,e){var n=e.descriptor;if("field"===e.kind){var i=e.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===i?void 0:i.call(t)}}Object.defineProperty(t,e.key,n)},decorateClass:function(t,e){var n=[],i=[],o={static:[],prototype:[],own:[]};if(t.forEach((function(t){this.addElementPlacement(t,o)}),this),t.forEach((function(t){if(!S(t))return n.push(t);var e=this.decorateElement(t,o);n.push(e.element),n.push.apply(n,e.extras),i.push.apply(i,e.finishers)}),this),!e)return{elements:n,finishers:i};var r=this.decorateConstructor(n,e);return i.push.apply(i,r.finishers),r.finishers=i,r},addElementPlacement:function(t,e,n){var i=e[t.placement];if(!n&&-1!==i.indexOf(t.key))throw new TypeError("Duplicated element ("+t.key+")");i.push(t.key)},decorateElement:function(t,e){for(var n=[],i=[],o=t.decorators,r=o.length-1;r>=0;r--){var a=e[t.placement];a.splice(a.indexOf(t.key),1);var s=this.fromElementDescriptor(t),l=this.toElementFinisherExtras((0,o[r])(s)||s);t=l.element,this.addElementPlacement(t,e),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var u=0;u<c.length;u++)this.addElementPlacement(c[u],e);n.push.apply(n,c)}}return{element:t,finishers:i,extras:n}},decorateConstructor:function(t,e){for(var n=[],i=e.length-1;i>=0;i--){var o=this.fromClassDescriptor(t),r=this.toClassDescriptor((0,e[i])(o)||o);if(void 0!==r.finisher&&n.push(r.finisher),void 0!==r.elements){t=r.elements;for(var a=0;a<t.length-1;a++)for(var s=a+1;s<t.length;s++)if(t[a].key===t[s].key&&t[a].placement===t[s].placement)throw new TypeError("Duplicated element ("+t[a].key+")")}}return{elements:t,finishers:n}},fromElementDescriptor:function(t){var e={kind:t.kind,key:t.key,placement:t.placement,descriptor:t.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===t.kind&&(e.initializer=t.initializer),e},toElementDescriptors:function(t){var e;if(void 0!==t)return(e=t,function(t){if(Array.isArray(t))return t}(e)||N(e)||z(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(t){var e=this.toElementDescriptor(t);return this.disallowProperty(t,"finisher","An element descriptor"),this.disallowProperty(t,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(t){var e=String(t.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var n=D(t.key),i=String(t.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=t.descriptor;this.disallowProperty(t,"elements","An element descriptor");var r={kind:e,key:n,placement:i,descriptor:Object.assign({},o)};return"field"!==e?this.disallowProperty(t,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),r.initializer=t.initializer),r},toElementFinisherExtras:function(t){return{element:this.toElementDescriptor(t),finisher:R(t,"finisher"),extras:this.toElementDescriptors(t.extras)}},fromClassDescriptor:function(t){var e={kind:"class",elements:t.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(t){var e=String(t.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(t,"key","A class descriptor"),this.disallowProperty(t,"placement","A class descriptor"),this.disallowProperty(t,"descriptor","A class descriptor"),this.disallowProperty(t,"initializer","A class descriptor"),this.disallowProperty(t,"extras","A class descriptor");var n=R(t,"finisher");return{elements:this.toElementDescriptors(t.elements),finisher:n}},runClassFinishers:function(t,e){for(var n=0;n<e.length;n++){var i=(0,e[n])(t);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");t=i}}return t},disallowProperty:function(t,e,n){if(void 0!==t[e])throw new TypeError(n+" can't have a ."+e+" property.")}};return t}();if(i)for(var r=0;r<i.length;r++)o=i[r](o);var a=e((function(t){o.initializeInstanceElements(t,s.elements)}),n),s=o.decorateClass(function(t){for(var e=[],n=function(t){return"method"===t.kind&&t.key===r.key&&t.placement===r.placement},i=0;i<t.length;i++){var o,r=t[i];if("method"===r.kind&&(o=e.find(n)))if(P(r.descriptor)||P(o.descriptor)){if(S(r)||S(o))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");o.descriptor=r.descriptor}else{if(S(r)){if(S(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");o.decorators=r.decorators}T(r,o)}else e.push(r)}return e}(a.d.map(A)),t);return o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([Object(i.d)("ha-voice-command-dialog")],(function(t,e){var n,u,_=function(e){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&O(t,e)}(o,e);var n,i=(n=o,function(){var t,e=M(n);if(j()){var i=M(this).constructor;t=Reflect.construct(e,arguments,i)}else t=e.apply(this,arguments);return C(this,t)});function o(){var e;x(this,o);for(var n=arguments.length,r=new Array(n),a=0;a<n;a++)r[a]=arguments[a];return e=i.call.apply(i,[this].concat(r)),t(E(e)),e}return o}(e);return{F:_,d:[{kind:"field",decorators:[Object(i.h)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[Object(i.h)()],key:"results",value:function(){return null}},{kind:"field",decorators:[Object(i.g)()],key:"_conversation",value:function(){return[{who:"hass",text:""}]}},{kind:"field",decorators:[Object(i.g)()],key:"_opened",value:function(){return!1}},{kind:"field",decorators:[Object(i.g)()],key:"_agentInfo",value:void 0},{kind:"field",decorators:[Object(i.i)("#messages")],key:"messages",value:void 0},{kind:"field",key:"recognition",value:void 0},{kind:"field",key:"_conversationId",value:void 0},{kind:"method",key:"showDialog",value:(u=w(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return this._opened=!0,a&&"https:"===location.protocol&&this._startListening(),t.next=4,this.hass.callWS({type:"conversation/agent/info"});case 4:this._agentInfo=t.sent;case 5:case"end":return t.stop()}}),t,this)}))),function(){return u.apply(this,arguments)})},{kind:"method",key:"render",value:function(){var t=this;return Object(i.f)(y(),this._opened,this._openedChanged,this._agentInfo&&this._agentInfo.onboarding?Object(i.f)(v(),this._agentInfo.onboarding.text,this._completeOnboarding,this._agentInfo.onboarding.url):"",Object(o.a)({"top-border":Boolean(this._agentInfo&&this._agentInfo.onboarding)}),this._conversation.map((function(e){return Object(i.f)(b(),t._computeMessageClasses(e),e.text)})),this.results?Object(i.f)(g(),Object(o.a)({interimTranscript:!this.results.final}),this.results.transcript,this.results.final?"":"…"):"",this._handleKeyUp,this.hass.localize("ui.dialogs.voice_command.".concat(a&&"https:"===location.protocol?"label_voice":"label")),a&&"https:"===location.protocol?Object(i.f)(m(),this.results?Object(i.f)(f()):"",this._toggleListening):"",this._agentInfo&&this._agentInfo.attribution?Object(i.f)(h(),this._agentInfo.attribution.url,this._agentInfo.attribution.name):"")}},{kind:"method",key:"firstUpdated",value:function(t){B(M(_.prototype),"updated",this).call(this,t),this._conversationId=s()+s()+s()+s()+s(),this._conversation=[{who:"hass",text:this.hass.localize("ui.dialogs.voice_command.how_can_i_help")}]}},{kind:"method",key:"updated",value:function(t){B(M(_.prototype),"updated",this).call(this,t),(t.has("_conversation")||t.has("results"))&&this._scrollMessagesBottom()}},{kind:"method",key:"_addMessage",value:function(t){this._conversation=[].concat(p(this._conversation),[t])}},{kind:"method",key:"_handleKeyUp",value:function(t){var e=t.target;13===t.keyCode&&e.value&&(this._processText(e.value),e.value="")}},{kind:"method",key:"_completeOnboarding",value:function(){var t,e;t=this.hass,e=!0,t.callWS({type:"conversation/onboarding/set",shown:e}),this._agentInfo=Object.assign({},this._agentInfo,{onboarding:void 0})}},{kind:"method",key:"_initRecognition",value:function(){var t=this;this.recognition=new a,this.recognition.interimResults=!0,this.recognition.lang="pl-PL",this.recognition.onstart=function(){t.results={final:!1,transcript:""}},this.recognition.onerror=function(e){if(t.recognition.abort(),"aborted"!==e.error){var n=t.results&&t.results.transcript?t.results.transcript:"<".concat(t.hass.localize("ui.dialogs.voice_command.did_not_hear"),">");t._addMessage({who:"user",text:n,error:!0})}t.results=null},this.recognition.onend=function(){if(null!=t.results){var e=t.results.transcript;t.results=null,e?t._processText(e):t._addMessage({who:"user",text:"<".concat(t.hass.localize("ui.dialogs.voice_command.did_not_hear"),">"),error:!0})}},this.recognition.onresult=function(e){var n=e.results[0];t.results={transcript:n[0].transcript,final:n.isFinal}}}},{kind:"method",key:"_processText",value:(n=w(regeneratorRuntime.mark((function t(e){var n,i,o;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return this.recognition&&this.recognition.abort(),this._addMessage({who:"user",text:e}),n={who:"hass",text:"…"},this._addMessage(n),t.prev=4,t.next=7,l(this.hass,e,this._conversationId);case 7:i=t.sent,o=i.speech.plain,n.text=o.speech,this.requestUpdate("_conversation"),t.next=18;break;case 13:t.prev=13,t.t0=t.catch(4),n.text=this.hass.localize("ui.dialogs.voice_command.error"),n.error=!0,this.requestUpdate("_conversation");case 18:case"end":return t.stop()}}),t,this,[[4,13]])}))),function(t){return n.apply(this,arguments)})},{kind:"method",key:"_toggleListening",value:function(){this.results?this.recognition.stop():this._startListening()}},{kind:"method",key:"_startListening",value:function(){this.recognition||this._initRecognition(),this.results||(this.results={transcript:"",final:!1},this.recognition.start())}},{kind:"method",key:"_scrollMessagesBottom",value:function(){this.messages.scrollTarget.scrollTop=this.messages.scrollTarget.scrollHeight,0===this.messages.scrollTarget.scrollTop&&Object(r.a)(this.messages,"iron-resize")}},{kind:"method",key:"_openedChanged",value:function(t){this._opened=t.detail.value,!this._opened&&this.recognition&&this.recognition.abort()}},{kind:"method",key:"_computeMessageClasses",value:function(t){return"message ".concat(t.who," ").concat(t.error?" error":"")}},{kind:"get",static:!0,key:"styles",value:function(){return[c.d,Object(i.c)(d())]}}]}}),i.a)}}]);
//# sourceMappingURL=chunk.82088f052f139a1243fa.js.map