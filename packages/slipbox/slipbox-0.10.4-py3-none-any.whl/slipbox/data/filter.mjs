#!/usr/bin/env node
import assert_1 from 'assert';
import require$$0 from 'fs';
import require$$0$1 from 'process';
import require$$1 from 'better-sqlite3';

var commonjsGlobal = typeof globalThis !== 'undefined' ? globalThis : typeof window !== 'undefined' ? window : typeof global !== 'undefined' ? global : typeof self !== 'undefined' ? self : {};

function getDefaultExportFromCjs (x) {
	return x && x.__esModule && Object.prototype.hasOwnProperty.call(x, 'default') ? x['default'] : x;
}

function createCommonjsModule(fn, basedir, module) {
	return module = {
	  path: basedir,
	  exports: {},
	  require: function (path, base) {
      return commonjsRequire(path, (base === undefined || base === null) ? module.path : base);
    }
	}, fn(module, module.exports), module.exports;
}

function commonjsRequire () {
	throw new Error('Dynamic requires are not currently supported by @rollup/plugin-commonjs');
}

var Alignment;
(function (Alignment) {
    Alignment[Alignment["AlignLeft"] = 0] = "AlignLeft";
    Alignment[Alignment["AlignRight"] = 1] = "AlignRight";
    Alignment[Alignment["AlignCenter"] = 2] = "AlignCenter";
    Alignment[Alignment["AlignDefault"] = 3] = "AlignDefault";
})(Alignment || (Alignment = {}));
var CitationMode;
(function (CitationMode) {
    CitationMode[CitationMode["AuthorInText"] = 0] = "AuthorInText";
    CitationMode[CitationMode["SuppressAuthor"] = 1] = "SuppressAuthor";
    CitationMode[CitationMode["NormalCitation"] = 2] = "NormalCitation";
})(CitationMode || (CitationMode = {}));
var ColWidth;
(function (ColWidth) {
    // ColWidth(number) // not supported
    ColWidth[ColWidth["ColWidthDefault"] = 0] = "ColWidthDefault";
})(ColWidth || (ColWidth = {}));
var ListNumberStyle;
(function (ListNumberStyle) {
    ListNumberStyle[ListNumberStyle["DefaultStyle"] = 0] = "DefaultStyle";
    ListNumberStyle[ListNumberStyle["Example"] = 1] = "Example";
    ListNumberStyle[ListNumberStyle["Decimal"] = 2] = "Decimal";
    ListNumberStyle[ListNumberStyle["LowerRoman"] = 3] = "LowerRoman";
    ListNumberStyle[ListNumberStyle["UpperRoman"] = 4] = "UpperRoman";
    ListNumberStyle[ListNumberStyle["LowerAlpha"] = 5] = "LowerAlpha";
    ListNumberStyle[ListNumberStyle["UpperAlpha"] = 6] = "UpperAlpha";
})(ListNumberStyle || (ListNumberStyle = {}));
var ListNumberDelim;
(function (ListNumberDelim) {
    ListNumberDelim[ListNumberDelim["DefaultDelim"] = 0] = "DefaultDelim";
    ListNumberDelim[ListNumberDelim["Period"] = 1] = "Period";
    ListNumberDelim[ListNumberDelim["OneParen"] = 2] = "OneParen";
    ListNumberDelim[ListNumberDelim["TwoParents"] = 3] = "TwoParents";
})(ListNumberDelim || (ListNumberDelim = {}));
var MathType;
(function (MathType) {
    MathType[MathType["DisplayMath"] = 0] = "DisplayMath";
    MathType[MathType["InlineMath"] = 1] = "InlineMath";
})(MathType || (MathType = {}));
var QuoteType;
(function (QuoteType) {
    QuoteType[QuoteType["SingleQuote"] = 0] = "SingleQuote";
    QuoteType[QuoteType["DoubleQuote"] = 1] = "DoubleQuote";
})(QuoteType || (QuoteType = {}));

var types = /*#__PURE__*/Object.freeze({
	__proto__: null,
	get Alignment () { return Alignment; },
	get CitationMode () { return CitationMode; },
	get ColWidth () { return ColWidth; },
	get ListNumberStyle () { return ListNumberStyle; },
	get ListNumberDelim () { return ListNumberDelim; },
	get MathType () { return MathType; },
	get QuoteType () { return QuoteType; }
});

function MetaBlocks(blocks) {
    return {
        t: 'MetaBlocks',
        c: blocks
    };
}
function MetaInlines(inlines) {
    return {
        t: 'MetaInlines',
        c: inlines
    };
}
function MetaList(values) {
    return {
        t: 'MetaList',
        c: values
    };
}
function MetaMap(map) {
    return {
        t: 'MetaMap',
        c: map
    };
}
function MetaBool(bool) {
    return {
        t: 'MetaBool',
        c: bool
    };
}
function MetaString(str) {
    return {
        t: 'MetaString',
        c: str
    };
}
function Pandoc(blocks, meta = {}) {
    return {
        meta: meta,
        blocks: blocks,
        'pandoc-api-version': [1, 21]
    };
}
function Attr(identifier = '', classes = [], attributes = {}) {
    return [identifier, classes, Object.entries(attributes)];
}
function Citation(id, mode, prefix, suffix, noteNum, hash) {
    return {
        citationId: id,
        citationPrefix: prefix,
        citationSuffix: suffix,
        citationMode: { t: CitationMode[mode] },
        citationNoteNum: noteNum,
        citationHash: hash
    };
}
function ListAttributes(start = 1, style = ListNumberStyle.DefaultStyle, delimiter = ListNumberDelim.DefaultDelim) {
    return [
        start,
        { t: ListNumberStyle[style] },
        { t: ListNumberDelim[delimiter] }
    ];
}
function Caption() {
    throw new Error('not implemented');
}
function ColSpec() {
    throw new Error('not implemented');
}
function TableHead() {
    throw new Error('not implemented');
}
function TableBody() {
    throw new Error('not implemented');
}
function TableFoot() {
    throw new Error('not implemented');
}
// Blocks
function BlockQuote(content) {
    return {
        t: 'BlockQuote',
        c: content
    };
}
function BulletList(content) {
    return {
        t: 'BulletList',
        c: content
    };
}
function CodeBlock(text, attr = Attr()) {
    return {
        t: 'CodeBlock',
        c: [attr, text]
    };
}
function DefinitionList(content) {
    return {
        t: 'DefinitionList',
        c: content
    };
}
function Div(content, attr = Attr()) {
    return {
        t: 'Div',
        c: [attr, content]
    };
}
function Header(level, content, attr = Attr()) {
    return {
        t: 'Header',
        c: [level, attr, content]
    };
}
function HorizontalRule() {
    return {
        t: 'HorizontalRule'
    };
}
function LineBlock(content) {
    return {
        t: 'LineBlock',
        c: content
    };
}
function Null() {
    return {
        t: 'Null'
    };
}
function OrderedList(content, listAttributes = ListAttributes()) {
    return {
        t: 'OrderedList',
        c: [listAttributes, content]
    };
}
function Para(content) {
    return {
        t: 'Para',
        c: content
    };
}
function Plain(content) {
    return {
        t: 'Plain',
        c: content
    };
}
function RawBlock(format, text) {
    return {
        t: 'RawBlock',
        c: [format, text]
    };
}
function Table(attr, caption, colspecs, head, bodies, foot) {
    return {
        t: 'Table',
        c: [attr, caption, colspecs, head, bodies, foot]
    };
}
// Inlines
function Cite(content, citations) {
    return {
        t: 'Cite',
        c: [citations, content]
    };
}
function Code(text, attr = Attr()) {
    return {
        t: 'Code',
        c: [attr, text]
    };
}
function Emph(content) {
    return {
        t: 'Emph',
        c: content
    };
}
function Image(caption, src, title = '', attr = Attr()) {
    return {
        t: 'Image',
        c: [attr, caption, [src, title]]
    };
}
function LineBreak() {
    return {
        t: 'LineBreak'
    };
}
function Link(content, target, title = '', attr = Attr()) {
    return {
        t: 'Link',
        c: [attr, content, [target, title]]
    };
}
function Math(mathtype, text) {
    return {
        t: 'Math',
        c: [{ t: MathType[mathtype] }, text]
    };
}
function Note(content) {
    return {
        t: 'Note',
        c: content
    };
}
function Quoted(quotetype, content) {
    return {
        t: 'Quoted',
        c: [{ t: QuoteType[quotetype] }, content]
    };
}
function RawInline(format, text) {
    return {
        t: 'RawInline',
        c: [format, text]
    };
}
function SmallCaps(content) {
    return {
        t: 'SmallCaps',
        c: content
    };
}
function SoftBreak() {
    return {
        t: 'SoftBreak'
    };
}
function Space() {
    return {
        t: 'Space'
    };
}
function Span(content, attr = Attr()) {
    return {
        t: 'Span',
        c: [attr, content]
    };
}
function Str(text) {
    return {
        t: 'Str',
        c: text
    };
}
function Strikeout(content) {
    return {
        t: 'Strikeout',
        c: content
    };
}
function Strong(content) {
    return {
        t: 'Strong',
        c: content
    };
}
function Subscript(content) {
    return {
        t: 'Subscript',
        c: content
    };
}
function Superscript(content) {
    return {
        t: 'Superscript',
        c: content
    };
}
function Underline(content) {
    return {
        t: 'Underline',
        c: content
    };
}

var create = /*#__PURE__*/Object.freeze({
	__proto__: null,
	MetaBlocks: MetaBlocks,
	MetaInlines: MetaInlines,
	MetaList: MetaList,
	MetaMap: MetaMap,
	MetaBool: MetaBool,
	MetaString: MetaString,
	Pandoc: Pandoc,
	Attr: Attr,
	Citation: Citation,
	ListAttributes: ListAttributes,
	Caption: Caption,
	ColSpec: ColSpec,
	TableHead: TableHead,
	TableBody: TableBody,
	TableFoot: TableFoot,
	BlockQuote: BlockQuote,
	BulletList: BulletList,
	CodeBlock: CodeBlock,
	DefinitionList: DefinitionList,
	Div: Div,
	Header: Header,
	HorizontalRule: HorizontalRule,
	LineBlock: LineBlock,
	Null: Null,
	OrderedList: OrderedList,
	Para: Para,
	Plain: Plain,
	RawBlock: RawBlock,
	Table: Table,
	Cite: Cite,
	Code: Code,
	Emph: Emph,
	Image: Image,
	LineBreak: LineBreak,
	Link: Link,
	Math: Math,
	Note: Note,
	Quoted: Quoted,
	RawInline: RawInline,
	SmallCaps: SmallCaps,
	SoftBreak: SoftBreak,
	Space: Space,
	Span: Span,
	Str: Str,
	Strikeout: Strikeout,
	Strong: Strong,
	Subscript: Subscript,
	Superscript: Superscript,
	Underline: Underline
});

function interact(filter) {
    const chunks = [];
    const readable = process.stdin;
    readable.on('readable', () => {
        for (;;) {
            const chunk = readable.read();
            if (chunk == null)
                break;
            chunks.push(chunk);
        }
    });
    readable.on('end', () => {
        const content = chunks.join('');
        let doc = JSON.parse(content);
        doc = applyFilter(doc, filter);
        console.log(JSON.stringify(doc));
    });
}
function applyFilter(doc, filter) {
    for (const fns of filter) {
        doc = applyFilterSet(doc, fns);
    }
    return doc;
}
function applyFilterSet(doc, fns) {
    doc.blocks = walkBlocks(doc.blocks, fns);
    doc.meta = fns.Meta ? fns.Meta(doc.meta) || doc.meta : doc.meta;
    return fns.Pandoc ? fns.Pandoc(doc) || doc : doc;
}
var walk;
(function (walk) {
    let inline;
    (function (inline) {
        function Cite(elem, fns) {
            elem.c[1] = walkInlines(elem.c[1], fns);
            return fns.Cite ? fns.Cite(elem) : elem;
        }
        inline.Cite = Cite;
        function Code(elem, fns) {
            return fns.Code ? fns.Code(elem) : elem;
        }
        inline.Code = Code;
        function Emph(elem, fns) {
            elem.c = walkInlines(elem.c, fns);
            return fns.Emph ? fns.Emph(elem) : elem;
        }
        inline.Emph = Emph;
        function Image(elem, fns) {
            elem.c[1] = walkInlines(elem.c[1], fns);
            return fns.Image ? fns.Image(elem) : elem;
        }
        inline.Image = Image;
        function LineBreak(elem, fns) {
            return fns.LineBreak ? fns.LineBreak(elem) : elem;
        }
        inline.LineBreak = LineBreak;
        function Link(elem, fns) {
            elem.c[1] = walkInlines(elem.c[1], fns);
            return fns.Link ? fns.Link(elem) : elem;
        }
        inline.Link = Link;
        function Math(elem, fns) {
            return fns.Math ? fns.Math(elem) : elem;
        }
        inline.Math = Math;
        function Note(elem, fns) {
            elem.c = walkBlocks(elem.c, fns);
            return fns.Note ? fns.Note(elem) : elem;
        }
        inline.Note = Note;
        function Quoted(elem, fns) {
            elem.c[1] = walkInlines(elem.c[1], fns);
            return fns.Quoted ? fns.Quoted(elem) : elem;
        }
        inline.Quoted = Quoted;
        function RawInline(elem, fns) {
            return fns.RawInline ? fns.RawInline(elem) : elem;
        }
        inline.RawInline = RawInline;
        function SmallCaps(elem, fns) {
            elem.c = walkInlines(elem.c, fns);
            return fns.SmallCaps ? fns.SmallCaps(elem) : elem;
        }
        inline.SmallCaps = SmallCaps;
        function SoftBreak(elem, fns) {
            return fns.SoftBreak ? fns.SoftBreak(elem) : elem;
        }
        inline.SoftBreak = SoftBreak;
        function Space(elem, fns) {
            return fns.Space ? fns.Space(elem) : elem;
        }
        inline.Space = Space;
        function Span(elem, fns) {
            elem.c[1] = walkInlines(elem.c[1], fns);
            return fns.Span ? fns.Span(elem) : elem;
        }
        inline.Span = Span;
        function Str(elem, fns) {
            return fns.Str ? fns.Str(elem) : elem;
        }
        inline.Str = Str;
        function Strikeout(elem, fns) {
            elem.c = walkInlines(elem.c, fns);
            return fns.Strikeout ? fns.Strikeout(elem) : elem;
        }
        inline.Strikeout = Strikeout;
        function Strong(elem, fns) {
            elem.c = walkInlines(elem.c, fns);
            return fns.Strong ? fns.Strong(elem) : elem;
        }
        inline.Strong = Strong;
        function Subscript(elem, fns) {
            elem.c = walkInlines(elem.c, fns);
            return fns.Subscript ? fns.Subscript(elem) : elem;
        }
        inline.Subscript = Subscript;
        function Superscript(elem, fns) {
            elem.c = walkInlines(elem.c, fns);
            return fns.Superscript ? fns.Superscript(elem) : elem;
        }
        inline.Superscript = Superscript;
        function Underline(elem, fns) {
            elem.c = walkInlines(elem.c, fns);
            return fns.Underline ? fns.Underline(elem) : elem;
        }
        inline.Underline = Underline;
    })(inline = walk.inline || (walk.inline = {}));
    let block;
    (function (block) {
        function BlockQuote(elem, fns) {
            elem.c = walkBlocks(elem.c, fns);
            return fns.BlockQuote ? fns.BlockQuote(elem) : elem;
        }
        block.BlockQuote = BlockQuote;
        function BulletList(elem, fns) {
            elem.c = elem.c.map(blocks => walkBlocks(blocks, fns));
            return fns.BulletList ? fns.BulletList(elem) : elem;
        }
        block.BulletList = BulletList;
        function CodeBlock(elem, fns) {
            return fns.CodeBlock ? fns.CodeBlock(elem) : elem;
        }
        block.CodeBlock = CodeBlock;
        function DefinitionList(elem, fns) {
            elem.c = elem.c.map(item => {
                const [inlines, blocksList] = item;
                return [
                    walkInlines(inlines, fns),
                    blocksList.map(blocks => walkBlocks(blocks, fns))
                ];
            });
            return fns.DefinitionList ? fns.DefinitionList(elem) : elem;
        }
        block.DefinitionList = DefinitionList;
        function Div(elem, fns) {
            elem.c[1] = walkBlocks(elem.c[1], fns);
            return fns.Div ? fns.Div(elem) : elem;
        }
        block.Div = Div;
        function Header(elem, fns) {
            elem.c[2] = walkInlines(elem.c[2], fns);
            return fns.Header ? fns.Header(elem) : elem;
        }
        block.Header = Header;
        function HorizontalRule(elem, fns) {
            return fns.HorizontalRule ? fns.HorizontalRule(elem) : elem;
        }
        block.HorizontalRule = HorizontalRule;
        function LineBlock(elem, fns) {
            elem.c = elem.c.map(inlines => walkInlines(inlines, fns));
            return fns.LineBlock ? fns.LineBlock(elem) : elem;
        }
        block.LineBlock = LineBlock;
        function Null(elem, fns) {
            return fns.Null ? fns.Null(elem) : elem;
        }
        block.Null = Null;
        function OrderedList(elem, fns) {
            elem.c[1] = elem.c[1].map(blocks => walkBlocks(blocks, fns));
            return fns.OrderedList ? fns.OrderedList(elem) : elem;
        }
        block.OrderedList = OrderedList;
        function Para(elem, fns) {
            elem.c = walkInlines(elem.c, fns);
            return fns.Para ? fns.Para(elem) : elem;
        }
        block.Para = Para;
        function Plain(elem, fns) {
            elem.c = walkInlines(elem.c, fns);
            return fns.Plain ? fns.Plain(elem) : elem;
        }
        block.Plain = Plain;
        function RawBlock(elem, fns) {
            return fns.RawBlock ? fns.RawBlock(elem) : elem;
        }
        block.RawBlock = RawBlock;
        function Table(elem, fns) {
            if (elem.c[1].c[0]) {
                elem.c[1].c[0] = walkInlines(elem.c[1].c[0], fns);
            }
            elem.c[1].c[1] = walkBlocks(elem.c[1].c[1], fns);
            for (const headRow of elem.c[3].c[1]) {
                for (const cell of headRow.c[1]) {
                    cell.c[4] = walkBlocks(cell.c[4], fns);
                }
            }
            for (const body of elem.c[4]) {
                for (const row of body.c[2]) {
                    for (const cell of row.c[1]) {
                        cell.c[4] = walkBlocks(cell.c[4], fns);
                    }
                }
                for (const row of body.c[3]) {
                    for (const cell of row.c[1]) {
                        cell.c[4] = walkBlocks(cell.c[4], fns);
                    }
                }
            }
            for (const footRow of elem.c[5].c[1]) {
                for (const cell of footRow.c[1]) {
                    cell.c[4] = walkBlocks(cell.c[4], fns);
                }
            }
            return fns.Table ? fns.Table(elem) : elem;
        }
        block.Table = Table;
    })(block = walk.block || (walk.block = {}));
})(walk || (walk = {}));
function walkInline(elem, fns) {
    const wi = walk.inline;
    const tag = elem.t;
    const visit = wi[tag];
    return visit(elem, fns);
}
function walkBlock(elem, fns) {
    const wb = walk.block;
    const tag = elem.t;
    const visit = wb[tag];
    return visit(elem, fns);
}
function walkInlines(elems, fns) {
    const result = [];
    for (const elem of elems) {
        const replacement = walkInline(elem, fns);
        if (replacement == null)
            result.push(elem);
        else if (replacement instanceof Array)
            result.push(...replacement);
        else
            result.push(replacement);
    }
    return result;
}
function walkBlocks(elems, fns) {
    const result = [];
    for (const elem of elems) {
        const replacement = walkBlock(elem, fns);
        if (replacement == null)
            result.push(elem);
        else if (replacement instanceof Array)
            result.push(...replacement);
        else
            result.push(replacement);
    }
    return result;
}

var filter = /*#__PURE__*/Object.freeze({
	__proto__: null,
	interact: interact,
	walkInline: walkInline,
	walkBlock: walkBlock,
	walkInlines: walkInlines,
	walkBlocks: walkBlocks
});

function identifier(elem) {
    if (elem instanceof Array) {
        return elem[0];
    }
    return identifier(attr(elem));
}
function classes(elem) {
    if (elem instanceof Array) {
        return elem[1];
    }
    return classes(attr(elem));
}
function attributes(elem) {
    if (elem instanceof Array) {
        return elem[2];
    }
    return attributes(attr(elem));
}
function id(citation) {
    return citation.citationId;
}
function mode(citation) {
    const tag = citation.citationMode.t;
    return CitationMode[tag];
}
function prefix(citation) {
    return citation.citationPrefix;
}
function suffix(citation) {
    return citation.citationSuffix;
}
function noteNum(citation) {
    return citation.citationNoteNum;
}
function hash(citation) {
    return citation.citationHash;
}
// Element properties
function attr(elem) {
    switch (elem.t) {
        case 'CodeBlock':
        case 'Div':
        case 'Table':
        case 'Code':
        case 'Image':
        case 'Link':
        case 'Span':
            return elem.c[0];
        case 'Header':
            return elem.c[1];
    }
}
function bodies(elem) {
    return elem.c[4];
}
function caption(elem) {
    return elem.c[1];
}
function citations(elem) {
    return elem.c[0];
}
function colspecs(elem) {
    return elem.c[2];
}
function content(elem) {
    switch (elem.t) {
        case 'BlockQuote':
        case 'BulletList':
        case 'DefinitionList':
        case 'LineBlock':
        case 'Para':
        case 'Plain':
        case 'Emph':
        case 'Note':
        case 'SmallCaps':
        case 'Strikeout':
        case 'Strong':
        case 'Subscript':
        case 'Superscript':
        case 'Underline':
            return elem.c;
        case 'Div':
        case 'OrderedList':
        case 'Cite':
        case 'Link':
        case 'Quoted':
        case 'Span':
            return elem.c[1];
        case 'Header':
            return elem.c[2];
    }
}
function delimiter(elem) {
    const tag = listAttributes(elem)[2].t;
    return ListNumberDelim[tag];
}
function foot(elem) {
    return elem.c[5];
}
function format(elem) {
    return elem.c[0];
}
function head(elem) {
    return elem.c[3];
}
function level(elem) {
    return elem.c[0];
}
function listAttributes(elem) {
    return elem.c[0];
}
function mathtype(elem) {
    const tag = elem.c[0].t;
    return MathType[tag];
}
function quotetype(elem) {
    const tag = elem.c[0].t;
    return QuoteType[tag];
}
function src(elem) {
    return elem.c[2][0];
}
function start(elem) {
    return listAttributes(elem)[0];
}
function style(elem) {
    const tag = listAttributes(elem)[1].t;
    return ListNumberStyle[tag];
}
function target(elem) {
    return elem.c[2][0];
}
function text(elem) {
    return elem.t === 'Str' ? elem.c : elem.c[1];
}
function title(elem) {
    return elem.c[2][1];
}

var get = /*#__PURE__*/Object.freeze({
	__proto__: null,
	identifier: identifier,
	classes: classes,
	attributes: attributes,
	id: id,
	mode: mode,
	prefix: prefix,
	suffix: suffix,
	noteNum: noteNum,
	hash: hash,
	attr: attr,
	bodies: bodies,
	caption: caption,
	citations: citations,
	colspecs: colspecs,
	content: content,
	delimiter: delimiter,
	foot: foot,
	format: format,
	head: head,
	level: level,
	listAttributes: listAttributes,
	mathtype: mathtype,
	quotetype: quotetype,
	src: src,
	start: start,
	style: style,
	target: target,
	text: text,
	title: title
});

function identifier$1(elem, val) {
    if (elem instanceof Array) {
        elem[0] = val;
    }
    else {
        identifier$1(attr(elem), val);
    }
}
function classes$1(elem, val) {
    if (elem instanceof Array) {
        elem[1] = val;
    }
    else {
        classes$1(attr(elem), val);
    }
}
function attributes$1(elem, val) {
    if (elem instanceof Array) {
        elem[2] = val;
    }
    else {
        attributes$1(attr(elem), val);
    }
}
function id$1(citation, val) {
    citation.citationId = val;
}
function mode$1(citation, val) {
    citation.citationMode.t = CitationMode[val];
}
function prefix$1(citation, val) {
    citation.citationPrefix = val;
}
function suffix$1(citation, val) {
    citation.citationSuffix = val;
}
function noteNum$1(citation, val) {
    citation.citationNoteNum = val;
}
function hash$1(citation, val) {
    citation.citationHash = val;
}
// Element properties
function attr$1(elem, val) {
    switch (elem.t) {
        case 'CodeBlock':
        case 'Div':
        case 'Table':
        case 'Code':
        case 'Image':
        case 'Link':
        case 'Span':
            elem.c[0] = val;
            break;
        case 'Header':
            elem.c[1] = val;
            break;
    }
}
function bodies$1(elem, val) {
    elem.c[4] = val;
}
function caption$1(elem, val) {
    elem.c[1] = val;
}
function citations$1(elem, val) {
    elem.c[0] = val;
}
function colspecs$1(elem, val) {
    elem.c[2] = val;
}
function content$1(elem, val) {
    switch (elem.t) {
        case 'BlockQuote':
        case 'Note':
            elem.c = val;
            break;
        case 'BulletList':
            elem.c = val;
            break;
        case 'DefinitionList':
            elem.c = val;
            break;
        case 'LineBlock':
            elem.c = val;
            break;
        case 'Para':
        case 'Plain':
        case 'Emph':
        case 'SmallCaps':
        case 'Strikeout':
        case 'Strong':
        case 'Subscript':
        case 'Superscript':
        case 'Underline':
            elem.c = val;
            break;
        case 'Div':
            elem.c[1] = val;
            break;
        case 'OrderedList':
            elem.c[1] = val;
            break;
        case 'Cite':
        case 'Link':
        case 'Quoted':
        case 'Span':
            elem.c[1] = val;
            break;
        case 'Header':
            elem.c[2] = val;
            break;
    }
}
function delimiter$1(elem, val) {
    listAttributes(elem)[2].t = ListNumberDelim[val];
}
function foot$1(elem, val) {
    elem.c[5] = val;
}
function format$1(elem, val) {
    elem.c[0] = val;
}
function head$1(elem, val) {
    elem.c[3] = val;
}
function level$1(elem, val) {
    elem.c[0] = val;
}
function listAttributes$1(elem, val) {
    elem.c[0] = val;
}
function mathtype$1(elem, val) {
    elem.c[0].t = MathType[val];
}
function quotetype$1(elem, val) {
    elem.c[0].t = QuoteType[val];
}
function src$1(elem, val) {
    elem.c[2][0] = val;
}
function start$1(elem, val) {
    listAttributes(elem)[0] = val;
}
function style$1(elem, val) {
    listAttributes(elem)[1].t = ListNumberStyle[val];
}
function target$1(elem, val) {
    elem.c[2][0] = val;
}
function text$1(elem, val) {
    if (elem.t === 'Str') {
        elem.c = val;
    }
    else {
        elem.c[1] = val;
    }
}
function title$1(elem, val) {
    elem.c[2][1] = val;
}
function withAttributes(elem, callback) {
    const attr = Object.fromEntries(attributes(elem));
    callback(attr);
    attributes$1(elem, Object.entries(attr));
}

var set = /*#__PURE__*/Object.freeze({
	__proto__: null,
	withAttributes: withAttributes,
	identifier: identifier$1,
	classes: classes$1,
	attributes: attributes$1,
	id: id$1,
	mode: mode$1,
	prefix: prefix$1,
	suffix: suffix$1,
	noteNum: noteNum$1,
	hash: hash$1,
	attr: attr$1,
	bodies: bodies$1,
	caption: caption$1,
	citations: citations$1,
	colspecs: colspecs$1,
	content: content$1,
	delimiter: delimiter$1,
	foot: foot$1,
	format: format$1,
	head: head$1,
	level: level$1,
	listAttributes: listAttributes$1,
	mathtype: mathtype$1,
	quotetype: quotetype$1,
	src: src$1,
	start: start$1,
	style: style$1,
	target: target$1,
	text: text$1,
	title: title$1
});

function concat(a, b) {
    return a + b;
}
function concatenate(a, b) {
    return a + stringify(b);
}
function concatenateInlines(elems) {
    return elems.reduce(concatenate, '');
}
function concatenateBlocks(elems) {
    return elems.reduce(concatenate, '');
}
var element;
(function (element) {
    function BlockQuote(elem) {
        return elem.c.reduce(concatenate, '');
    }
    element.BlockQuote = BlockQuote;
    function BulletList(elem) {
        return elem.c.map(concatenateBlocks).reduce(concat, '');
    }
    element.BulletList = BulletList;
    function CodeBlock(elem) {
        return elem.c[1];
    }
    element.CodeBlock = CodeBlock;
    function DefinitionList(elem) {
        return elem.c.map(([inlines, blocksList]) => {
            return concatenateInlines(inlines) + blocksList.map(concatenateBlocks).reduce(concat, '');
        }).reduce(concat, '');
    }
    element.DefinitionList = DefinitionList;
    function Div(elem) {
        return concatenateBlocks(elem.c[1]);
    }
    element.Div = Div;
    function Header(elem) {
        return concatenateInlines(elem.c[2]);
    }
    element.Header = Header;
    function HorizontalRule(elem) {
        return '';
    }
    element.HorizontalRule = HorizontalRule;
    function LineBlock(elem) {
        return elem.c.map(concatenateInlines).reduce(concat, '');
    }
    element.LineBlock = LineBlock;
    function Null(elem) {
        return '';
    }
    element.Null = Null;
    function OrderedList(elem) {
        return elem.c[1].map(concatenateBlocks).reduce(concat, '');
    }
    element.OrderedList = OrderedList;
    function Para(elem) {
        return concatenateInlines(elem.c);
    }
    element.Para = Para;
    function Plain(elem) {
        return concatenateInlines(elem.c);
    }
    element.Plain = Plain;
    function RawBlock(elem) {
        return elem.c[1];
    }
    element.RawBlock = RawBlock;
    function Table(elem) {
        throw new Error('not implemented');
    }
    element.Table = Table;
    function Cite(elem) {
        return concatenateInlines(elem.c[1]);
    }
    element.Cite = Cite;
    function Code(elem) {
        return elem.c[1];
    }
    element.Code = Code;
    function Emph(elem) {
        return concatenateInlines(elem.c);
    }
    element.Emph = Emph;
    function Image(elem) {
        return concatenateInlines(elem.c[1]);
    }
    element.Image = Image;
    function LineBreak(elem) {
        return ' ';
    }
    element.LineBreak = LineBreak;
    function Link(elem) {
        return concatenateInlines(elem.c[1]);
    }
    element.Link = Link;
    function Math(elem) {
        return elem.c[1];
    }
    element.Math = Math;
    function Note(elem) {
        return concatenateBlocks(elem.c);
    }
    element.Note = Note;
    function Quoted(elem) {
        const content = concatenateInlines(elem.c[1]);
        switch (quotetype(elem)) {
            case QuoteType.SingleQuote:
                return `‘${content}’`;
            case QuoteType.DoubleQuote:
                return `“${content}”`;
        }
        throw new Error('unreachable');
    }
    element.Quoted = Quoted;
    function RawInline(elem) {
        return elem.c[1];
    }
    element.RawInline = RawInline;
    function SmallCaps(elem) {
        return concatenateInlines(elem.c);
    }
    element.SmallCaps = SmallCaps;
    function SoftBreak(elem) {
        return ' ';
    }
    element.SoftBreak = SoftBreak;
    function Space(elem) {
        return ' ';
    }
    element.Space = Space;
    function Span(elem) {
        return concatenateInlines(elem.c[1]);
    }
    element.Span = Span;
    function Str(elem) {
        return elem.c;
    }
    element.Str = Str;
    function Strikeout(elem) {
        return concatenateInlines(elem.c);
    }
    element.Strikeout = Strikeout;
    function Strong(elem) {
        return concatenateInlines(elem.c);
    }
    element.Strong = Strong;
    function Subscript(elem) {
        return concatenateInlines(elem.c);
    }
    element.Subscript = Subscript;
    function Superscript(elem) {
        return concatenateInlines(elem.c);
    }
    element.Superscript = Superscript;
    function Underline(elem) {
        return concatenateInlines(elem.c);
    }
    element.Underline = Underline;
    function Pandoc(doc) {
        return concatenateBlocks(doc.blocks);
    }
    element.Pandoc = Pandoc;
})(element || (element = {}));
function isDocument(elem) {
    return !elem.t;
}
function stringify(elem) {
    if (isDocument(elem))
        return element.Pandoc(elem);
    const tag = elem.t;
    const fn = element[tag];
    return fn(elem);
}

function findNext(elems, cond, start = 0, end = -1) {
    if (end < 0) {
        end = elems.length;
    }
    for (let i = start; i < end; i++) {
        if (cond(elems[i])) {
            return i;
        }
    }
    return end;
}
function isTopLevel(elem) {
    return elem.t === 'Header' && level(elem) === 1;
}
function makeTopLevelSections(blocks, fn) {
    // fn creates an Attr from the header for its parent Div.
    let prev = findNext(blocks, isTopLevel);
    while (prev < blocks.length) {
        const next = findNext(blocks, isTopLevel, prev + 1);
        if (prev < next) {
            const block = blocks[prev];
            const div = Div([], fn(block));
            const slice = blocks.splice(prev, next - prev, div);
            content$1(div, slice);
        }
        prev++;
    }
    return blocks;
}

var utils = /*#__PURE__*/Object.freeze({
	__proto__: null,
	makeTopLevelSections: makeTopLevelSections,
	stringify: stringify
});

var src$2 = /*#__PURE__*/Object.freeze({
	__proto__: null,
	create: create,
	filter: filter,
	get: get,
	set: set,
	types: types,
	utils: utils,
	interact: interact,
	withAttributes: withAttributes
});

var utils$1 = createCommonjsModule(function (module, exports) {
var __createBinding = (commonjsGlobal && commonjsGlobal.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (commonjsGlobal && commonjsGlobal.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (commonjsGlobal && commonjsGlobal.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseLink = exports.parseHeaderText = exports.parseFilename = exports.parentAlias = exports.isTopLevelSection = exports.isReferenceId = exports.hashtagPrefix = exports.fileToBase64 = exports.fileExtension = void 0;
var fs = __importStar(require$$0);

var NUMBER_PATTERN = /^\d+$/;
var NUMBER_REGEX = new RegExp(NUMBER_PATTERN);
function isTopLevelSection(div) {
    return NUMBER_REGEX.test(src$2.get.identifier(div)) && src$2.get.classes(div).includes('level1');
}
exports.isTopLevelSection = isTopLevelSection;
// TODO shouldn't the pattern be /^.+(\..+)$/
var FILENAME_EXTENSION_PATTERN = /^.+(\..*)$/;
var FILENAME_EXTENSION_REGEX = new RegExp(FILENAME_EXTENSION_PATTERN);
function fileExtension(filename) {
    var result = FILENAME_EXTENSION_REGEX.exec(filename);
    return result == null ? '' : result[1].slice(1);
}
exports.fileExtension = fileExtension;
var HASHTAG_PATTERN = /^#+[-_a-zA-Z0-9]+/;
var HASHTAG_REGEX = new RegExp(HASHTAG_PATTERN);
function hashtagPrefix(text) {
    var result = HASHTAG_REGEX.exec(text);
    return result == null ? null : result[0];
}
exports.hashtagPrefix = hashtagPrefix;
var HEADER_PATTERN = /^\s*(\d+)\s+(.+?)\s*$/;
var HEADER_REGEX = new RegExp(HEADER_PATTERN);
function parseHeaderText(text) {
    var result = HEADER_REGEX.exec(text);
    if (result != null && result.length === 3) {
        HEADER_REGEX.lastIndex = 0;
        return { id: Number(result[1]), title: result[2] };
    }
    return { id: null, title: null };
}
exports.parseHeaderText = parseHeaderText;
var TARGET_PATTERN = /^#\d+$/;
var TARGET_REGEX = new RegExp(TARGET_PATTERN);
var SEQUENCE_PATTERN = /^\/[a-zA-Z][a-zA-Z0-9]*$/;
var SEQUENCE_REGEX = new RegExp(SEQUENCE_PATTERN);
function parseLink(src, elem) {
    var target = src$2.get.target(elem);
    if (!NUMBER_REGEX.exec(src))
        return;
    if (!TARGET_REGEX.exec(target))
        return;
    var dest = target.slice(1);
    var title = src$2.get.title(elem);
    if (!SEQUENCE_REGEX.exec(title)) {
        return { src: src, dest: dest, tag: 'direct', description: title };
    }
    return { src: src, dest: dest, tag: 'sequence', description: src + title.slice(1) };
}
exports.parseLink = parseLink;
var RAWBLOCK_PATTERN = /^<!--#slipbox-metadata\nfilename: (.+?)\n-->$/;
var RAWBLOCK_REGEX = new RegExp(RAWBLOCK_PATTERN);
function parseFilename(elem) {
    var result = RAWBLOCK_REGEX.exec(src$2.get.text(elem));
    if (result && result.length > 1) {
        return result[1];
    }
}
exports.parseFilename = parseFilename;
var ALIAS_PATTERN_A = /^(\d+[\da-z]*?)[a-z]+$/;
var ALIAS_REGEX_A = new RegExp(ALIAS_PATTERN_A);
var ALIAS_PATTERN_D = /^(\d+[\da-z]*?)\d+$/;
var ALIAS_REGEX_D = new RegExp(ALIAS_PATTERN_D);
function parentAlias(alias) {
    var result = ALIAS_REGEX_A.exec(alias);
    if (result && result.length > 1) {
        return result[1];
    }
    result = ALIAS_REGEX_D.exec(alias);
    if (result && result.length > 1) {
        return result[1];
    }
    return null;
}
exports.parentAlias = parentAlias;
var REFERENCE_ID_PATTERN = /^ref-.+$/;
var REFERENCE_ID_REGEX = new RegExp(REFERENCE_ID_PATTERN);
function isReferenceId(id) {
    return REFERENCE_ID_REGEX.test(id);
}
exports.isReferenceId = isReferenceId;
var CACHE = {};
function fileToBase64(path) {
    if (CACHE[path] != null)
        return CACHE[path];
    var content = fs.readFileSync(path, 'utf-8');
    CACHE[path] = Buffer.from(content, 'utf-8').toString('base64');
    return CACHE[path];
}
exports.fileToBase64 = fileToBase64;
});

var log = createCommonjsModule(function (module, exports) {
Object.defineProperty(exports, "__esModule", { value: true });
exports.warning = void 0;

function warning(messages) {
    assert_1.strict(messages.length > 0);
    console.error("[WARNING] " + messages[0]);
    for (var i = 1; i < messages.length; i++) {
        console.error("  " + messages[i]);
    }
}
exports.warning = warning;
});

var slipbox = createCommonjsModule(function (module, exports) {
var __createBinding = (commonjsGlobal && commonjsGlobal.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (commonjsGlobal && commonjsGlobal.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (commonjsGlobal && commonjsGlobal.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (commonjsGlobal && commonjsGlobal.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Slipbox = void 0;

var process = __importStar(require$$0$1);
var better_sqlite3_1 = __importDefault(require$$1);


var Slipbox = /** @class */ (function () {
    function Slipbox() {
        this.notes = {};
        this.citations = {};
        this.aliases = {};
        this.sequences = [];
        this.links = [];
        this.tags = [];
        this.references = [];
        this.errors = { hasEmptyLink: new Set() };
        var path = process.env.SLIPBOX_DB || 'slipbox.db';
        this.db = new better_sqlite3_1.default(path, { fileMustExist: true });
        var db = this.db;
        this.insert = {
            alias: db.prepare('INSERT OR IGNORE INTO Aliases (id, owner, alias) VALUES (?, ?, ?)'),
            bib: db.prepare('INSERT OR IGNORE INTO Bibliography (key, text) VALUES (?, ?)'),
            cite: db.prepare('INSERT INTO Citations (note, reference) VALUES (?, ?)'),
            file: db.prepare('INSERT OR IGNORE INTO Files (filename) VALUES (?)'),
            link: db.prepare('INSERT INTO Links (src, dest, annotation) VALUES (?, ?, ?)'),
            note: db.prepare('INSERT INTO Notes (id, title, filename) VALUES (?, ?, ?)'),
            sequence: db.prepare('INSERT OR IGNORE INTO Sequences (prev, next) VALUES (?, ?)'),
            tag: db.prepare('INSERT OR IGNORE INTO Tags (id, tag) VALUES (?, ?)')
        };
        this.update = {
            bib: db.prepare('UPDATE Bibliography SET text = ? WHERE key = ?')
        };
        this.select = {
            note: db.prepare('SELECT id, title, filename FROM Notes WHERE id = ?'),
            noteFromAlias: db.prepare('SELECT id, title, filename FROM Notes JOIN Aliases USING (id) WHERE alias = ?')
        };
    }
    Slipbox.prototype.saveNote = function (id, title, filename) {
        var existing = this.notes[id];
        if (existing == null) {
            this.notes[id] = { title: title, filename: filename };
        }
        else {
            log.warning([
                "Duplicate ID: " + id + ".",
                "Could not insert note '" + title + "'.",
                "Note '" + existing.title + "' already uses the ID."
            ]);
        }
    };
    Slipbox.prototype.saveCite = function (id, ref) {
        var rec = new Set(this.citations[id] || []);
        rec.add('ref-' + ref);
        this.citations[id] = rec;
    };
    Slipbox.prototype.saveAlias = function (alias, id, owner) {
        var existing = this.aliases[alias];
        if (existing && existing.id !== id) {
            log.warning([
                "Duplicate alias definition for '" + alias + "' used by note " + existing.id + ".",
                "It will not be used as an alias for note " + id + "."
            ]);
        }
        else {
            this.aliases[alias] = { id: id, owner: owner };
            var prev = utils$1.parentAlias(alias);
            if (prev != null) {
                this.sequences.push([prev, alias]);
            }
        }
    };
    Slipbox.prototype.saveLink = function (src, dest, description) {
        this.links.push({ tag: 'direct', src: src, dest: dest, description: description });
    };
    Slipbox.prototype.saveTag = function (id, tag) {
        this.tags.push([id, tag]);
    };
    Slipbox.prototype.saveNotes = function () {
        var _this = this;
        var insertMany = this.db.transaction(function () {
            for (var _i = 0, _a = Object.entries(_this.notes); _i < _a.length; _i++) {
                var note = _a[_i];
                var id = note[0], _b = note[1], title = _b.title, filename = _b.filename;
                _this.insert.file.run(filename);
                try {
                    _this.insert.note.run([id, title, filename]);
                }
                catch (error) {
                    var existing = _this.select.note.get(id);
                    assert_1.strict(existing);
                    var messages = [
                        "Duplicate ID: " + id + ".",
                        "Could not insert note '" + title + "'.",
                        "Note '" + existing.title + "' already uses the ID.",
                        "See '" + filename + "' or '" + existing.filename + "'."
                    ];
                    log.warning(messages);
                }
            }
        });
        insertMany();
        this.notes = {}; // ???
    };
    Slipbox.prototype.saveCitations = function () {
        var _this = this;
        var insertMany = this.db.transaction(function () {
            var _loop_1 = function (id, _cites) {
                _cites.forEach(function (cite) {
                    _this.insert.bib.run([cite, '']);
                    _this.insert.cite.run([id, cite]);
                });
            };
            for (var _i = 0, _a = Object.entries(_this.citations); _i < _a.length; _i++) {
                var _b = _a[_i], id = _b[0], _cites = _b[1];
                _loop_1(id, _cites);
            }
        });
        insertMany();
        this.citations = {}; // ???
    };
    Slipbox.prototype.saveAliases = function () {
        var _this = this;
        var insertMany = this.db.transaction(function () {
            for (var _i = 0, _a = Object.entries(_this.aliases); _i < _a.length; _i++) {
                var _b = _a[_i], alias = _b[0], _c = _b[1], id = _c.id, owner = _c.owner;
                _this.insert.alias.run([owner, owner, String(owner)]);
                _this.insert.alias.run([id, owner, alias]);
            }
        });
        insertMany();
        this.aliases = {}; // ???
    };
    Slipbox.prototype.saveSequences = function () {
        var _this = this;
        var insertMany = this.db.transaction(function () {
            for (var _i = 0, _a = _this.sequences; _i < _a.length; _i++) {
                var _b = _a[_i], prev = _b[0], next = _b[1];
                assert_1.strict(prev && next);
                try {
                    _this.insert.sequence.run([prev, next]);
                }
                catch (error) {
                    // NOTE assume prev is the missing alias
                    var existing = _this.select.noteFromAlias.get(next);
                    assert_1.strict(existing);
                    log.warning([
                        "Missing note alias: '" + prev + "'.",
                        "Note " + existing.id + " with alias '" + next + "' will be unreachable."
                    ]);
                    // TODO What if note with parent alias with be added in the
                    // next batch (i.e. has different file extension)?
                }
            }
        });
        insertMany();
        this.sequences = []; // ???
    };
    Slipbox.prototype.saveLinks = function () {
        var _this = this;
        // TODO handle error if note has duplicate links to a note
        var insertMany = this.db.transaction(function () {
            for (var _i = 0, _a = _this.links; _i < _a.length; _i++) {
                var _b = _a[_i], tag = _b.tag, src = _b.src, dest = _b.dest, description = _b.description;
                assert_1.strict(tag === 'direct');
                _this.insert.link.run([src, dest, description]);
            }
        });
        insertMany();
        this.links = []; // ???
    };
    Slipbox.prototype.saveTags = function () {
        var _this = this;
        var insertMany = this.db.transaction(function () {
            for (var _i = 0, _a = _this.tags; _i < _a.length; _i++) {
                var _b = _a[_i], id = _b[0], tag = _b[1];
                _this.insert.tag.run([id, tag]);
            }
        });
        insertMany();
        this.tags = []; // ???
    };
    Slipbox.prototype.saveReferences = function (references) {
        var _this = this;
        var insertMany = this.db.transaction(function () {
            for (var _i = 0, references_1 = references; _i < references_1.length; _i++) {
                var _a = references_1[_i], key = _a[0], text = _a[1];
                _this.update.bib.run([text, key]);
            }
        });
        insertMany();
    };
    Slipbox.prototype.hasEmptyLink = function (id) {
        this.errors.hasEmptyLink.add(id);
    };
    Slipbox.prototype.checkEmptyLinks = function () {
        var ids = Array.from(this.errors.hasEmptyLink).map(function (x) { return "'" + x + "'"; }).join(', ');
        var result = this.db.prepare("\n      SELECT id, title, filename\n      FROM Notes\n      WHERE id IN (" + ids + ")\n      ORDER BY id\n    ").all();
        var messages = ['The notes below contain links with an empty target.'];
        for (var _i = 0, result_1 = result; _i < result_1.length; _i++) {
            var _a = result_1[_i], id = _a.id, title = _a.title, filename = _a.filename;
            messages.push(id + ". " + title + " in '" + filename + "'.");
        }
        if (messages.length > 1) {
            log.warning(messages);
        }
    };
    return Slipbox;
}());
exports.Slipbox = Slipbox;
});

var build = createCommonjsModule(function (module, exports) {
var __createBinding = (commonjsGlobal && commonjsGlobal.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (commonjsGlobal && commonjsGlobal.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (commonjsGlobal && commonjsGlobal.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });


var process = __importStar(require$$0$1);



var makeTopLevelSections = src$2.utils.makeTopLevelSections, stringify = src$2.utils.stringify;
var interact = src$2.filter.interact, walkBlocks = src$2.filter.walkBlocks;
function preprocess() {
    function Pandoc(doc) {
        var filename = '';
        for (var _i = 0, _a = doc.blocks; _i < _a.length; _i++) {
            var elem = _a[_i];
            if (elem.t === 'RawBlock') {
                if (src$2.get.format(elem) === 'html') {
                    filename = utils$1.parseFilename(elem) || filename;
                }
            }
            else if (elem.t === 'Header') {
                if (src$2.get.level(elem) === 1) {
                    assert_1.strict(filename);
                    src$2.get.attributes(elem).push(['filename', filename]);
                }
            }
        }
        return doc;
    }
    return { Pandoc: Pandoc };
}
function init(slipbox) {
    function RawBlock(elem) {
        if (src$2.get.format(elem) === 'html' && utils$1.parseFilename(elem)) {
            return [];
        }
    }
    function Header(elem) {
        if (src$2.get.level(elem) !== 1)
            return;
        var content = stringify(elem);
        var _a = utils$1.parseHeaderText(content), id = _a.id, title = _a.title;
        if (id != null && title != null) {
            src$2.set.identifier(elem, String(id));
            var filename_1 = '';
            src$2.withAttributes(elem, function (attr) {
                attr.title = title;
                filename_1 = attr.filename;
                delete attr.filename;
            });
            assert_1.strict(filename_1);
            slipbox.saveNote(src$2.get.identifier(elem), title, filename_1);
            return elem;
        }
    }
    function Pandoc(doc) {
        doc.blocks = makeTopLevelSections(doc.blocks, function (header) { return src$2.create.Attr(src$2.get.identifier(header), ['level1']); });
        slipbox.saveNotes();
        return doc;
    }
    return { Header: Header, RawBlock: RawBlock, Pandoc: Pandoc };
}
function collect(slipbox) {
    function Div(div) {
        if (!utils$1.isTopLevelSection(div))
            return;
        var hasEmptyLink = false;
        function Cite(elem) {
            for (var _i = 0, _a = Object.values(src$2.get.citations(elem)); _i < _a.length; _i++) {
                var citation = _a[_i];
                slipbox.saveCite(src$2.get.identifier(div), src$2.get.id(citation));
            }
        }
        function Link(elem) {
            if (!src$2.get.target(elem)) {
                hasEmptyLink = true;
                return src$2.get.content(elem);
            }
            var identifier = src$2.get.identifier(div);
            var link = utils$1.parseLink(identifier, elem);
            if (!link)
                return;
            if (link.tag === 'direct') {
                slipbox.saveLink(link.src, link.dest, link.description);
            }
            else if (link.tag === 'sequence') {
                slipbox.saveAlias(link.description, link.dest, link.src);
            }
        }
        function Str(elem) {
            var text = src$2.get.text(elem);
            if (utils$1.hashtagPrefix(text)) {
                slipbox.saveTag(src$2.get.identifier(div), text);
            }
        }
        var filter = { Cite: Cite, Link: Link, Str: Str };
        src$2.set.content(div, walkBlocks(src$2.get.content(div), filter));
        if (hasEmptyLink) {
            slipbox.hasEmptyLink(src$2.get.identifier(div));
        }
        return div;
    }
    function Pandoc(doc) {
        slipbox.saveAliases();
        slipbox.saveSequences();
        slipbox.saveCitations();
        slipbox.saveLinks();
        slipbox.saveTags();
        return doc;
    }
    return { Div: Div, Pandoc: Pandoc };
}
function modify(slipbox) {
    function Div(div) {
        if (!utils$1.isTopLevelSection(div))
            return;
        function Link(elem) {
            var content = stringify(elem);
            if (!content) {
                var target = src$2.get.target(elem);
                return [
                    src$2.create.Str(' ['),
                    src$2.create.Link([src$2.create.Str(target)], target, src$2.get.title(elem)),
                    src$2.create.Str(']')
                ];
            }
        }
        function Str(elem) {
            var text = src$2.get.text(elem);
            if (utils$1.hashtagPrefix(text)) {
                var src = '#' + text;
                return src$2.create.Link([elem], src);
            }
        }
        var footnotes = [];
        function Note(elem) {
            footnotes.push(src$2.create.Div(src$2.get.content(elem)));
            return src$2.create.Superscript([src$2.create.Str(String(footnotes.length))]);
        }
        var filter = { Link: Link, Note: Note, Str: Str };
        src$2.set.content(div, walkBlocks(src$2.get.content(div), filter));
        if (footnotes.length > 0) {
            // insert footnotes into document
            src$2.get.content(div).push(src$2.create.HorizontalRule());
            src$2.get.content(div).push(src$2.create.OrderedList(footnotes.map(function (fn) { return [fn]; })));
        }
        if (src$2.get.classes(div).includes('level1')) {
            // hide sections
            src$2.get.attributes(div).push(['style', 'display:none']);
        }
        return div;
    }
    return { Div: Div };
}
function citations(slipbox) {
    var references = [];
    function Div(div) {
        if (src$2.get.identifier(div) === 'refs') {
            walkBlocks(src$2.get.content(div), {
                Div: function (elem) {
                    var id = src$2.get.identifier(elem);
                    if (utils$1.isReferenceId(id)) {
                        references.push([id, stringify(elem)]);
                    }
                }
            });
            return [];
        }
    }
    function Pandoc(doc) {
        slipbox.saveReferences(references);
        return doc;
    }
    return { Div: Div, Pandoc: Pandoc };
}
function images() {
    var convert = process.env.CONVERT_TO_DATA_URL;
    if (!convert)
        return {};
    return {
        Image: function (elem) {
            var src = src$2.get.src(elem);
            if (!require$$0.existsSync(src))
                return;
            var ext = utils$1.fileExtension(src);
            if (ext) {
                var base64 = utils$1.fileToBase64(src);
                src$2.set.src(elem, "data:image/" + ext + ";base64," + base64);
                return elem;
            }
        }
    };
}
function commit(slipbox) {
    function Pandoc(doc) {
        slipbox.checkEmptyLinks();
        return doc;
    }
    return { Pandoc: Pandoc };
}
function main() {
    var slipbox$1 = new slipbox.Slipbox();
    var filters = [
        preprocess(),
        init(slipbox$1),
        collect(slipbox$1),
        modify(),
        citations(slipbox$1),
        images(),
        commit(slipbox$1)
    ];
    interact(filters);
}
main();
});

var index = /*@__PURE__*/getDefaultExportFromCjs(build);

export default index;
