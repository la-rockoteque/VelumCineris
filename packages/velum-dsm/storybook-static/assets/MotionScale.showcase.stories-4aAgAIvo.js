import{j as e,m as a}from"./iframe-v_xVpIIQ.js";import{S as c,a as m,b as t}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const y={title:"Tokens/MotionScale"},i=l=>({width:"120px",height:"12px",borderRadius:"999px",background:"linear-gradient(90deg, var(--accent-soft), var(--accent))",animation:`pulse ${l} infinite alternate`}),s={render:()=>e.jsxs(c,{children:[e.jsx("style",{children:"@keyframes pulse { from { transform: scaleX(0.55); opacity: 0.5; } to { transform: scaleX(1); opacity: 1; } }"}),e.jsxs(m,{children:[e.jsx(t,{label:"Quick",description:a.quick,children:e.jsx("div",{style:i(a.quick)})}),e.jsx(t,{label:"Base",description:a.base,children:e.jsx("div",{style:i(a.base)})}),e.jsx(t,{label:"Slow",description:a.slow,children:e.jsx("div",{style:i(a.slow)})}),e.jsx(t,{label:"Easing",description:JSON.stringify(a.easing),minHeight:"96px",children:e.jsx("div",{style:{fontFamily:"var(--velum-font-mono)",fontSize:"0.82rem"},children:JSON.stringify(a.easing)})})]})]})};var n,o,r;s.parameters={...s.parameters,docs:{...(n=s.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame>
      <style>{\`@keyframes pulse { from { transform: scaleX(0.55); opacity: 0.5; } to { transform: scaleX(1); opacity: 1; } }\`}</style>
      <StateMatrix>
        <StateCase label="Quick" description={motionScale.quick}>
          <div style={bar(motionScale.quick)} />
        </StateCase>
        <StateCase label="Base" description={motionScale.base}>
          <div style={bar(motionScale.base)} />
        </StateCase>
        <StateCase label="Slow" description={motionScale.slow}>
          <div style={bar(motionScale.slow)} />
        </StateCase>
        <StateCase label="Easing" description={JSON.stringify(motionScale.easing)} minHeight="96px">
          <div style={{
          fontFamily: "var(--velum-font-mono)",
          fontSize: "0.82rem"
        }}>{JSON.stringify(motionScale.easing)}</div>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(r=(o=s.parameters)==null?void 0:o.docs)==null?void 0:r.source}}};const f=["Showcase"];export{s as Showcase,f as __namedExportsOrder,y as default};
