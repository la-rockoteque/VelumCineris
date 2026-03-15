import{j as a}from"./jsx-runtime-Bll8AAhy.js";import{C as o,S as s}from"./VelumProvider-Cnx-m3OC.js";import{S as c,a as n,b as m}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const w={title:"Assets/SigilMark"},d=[{label:"Small",width:"48px",color:"var(--accent-soft)"},{label:"Default",width:"88px",color:"var(--accent)"},{label:"Large",width:"132px",color:"var(--ink)"}],r={render:()=>a.jsx(c,{maxWidth:"980px",children:a.jsx(o,{title:"Sigil Mark Showcase",subtitle:"Scale and tone variations for the primary emblem.",children:a.jsx(n,{children:d.map(e=>a.jsx(m,{label:e.label,description:`${e.width} · ${e.color.replace("var(","").replace(")","")}`,minHeight:"120px",children:a.jsx(s,{style:{width:e.width,color:e.color}})},e.label))})})})};var t,i,l;r.parameters={...r.parameters,docs:{...(t=r.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <Card title="Sigil Mark Showcase" subtitle="Scale and tone variations for the primary emblem.">
        <StateMatrix>
          {cases.map(item => <StateCase key={item.label} label={item.label} description={\`\${item.width} · \${item.color.replace("var(", "").replace(")", "")}\`} minHeight="120px">
              <SigilMark style={{
            width: item.width,
            color: item.color
          }} />
            </StateCase>)}
        </StateMatrix>
      </Card>
    </StoryFrame>
}`,...(l=(i=r.parameters)==null?void 0:i.docs)==null?void 0:l.source}}};const g=["Showcase"];export{r as Showcase,g as __namedExportsOrder,w as default};
