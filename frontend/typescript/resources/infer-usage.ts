export type a = {
    aa_a: string;
    bB_B: number;
};

export type b = {
    aaA: string;
    bBB: number;
};

export type CamelCase<T> = {
    [K in keyof T as K extends string ? CamelCaseString<K> : K]: T[K]
};

export type CamelCaseString<S extends string> = S extends `${infer T}_${infer U}` ? `${Uncapitalize<T>}${Capitalize<U>}` : S;

export class Test {
    public test: CamelCase<a>;

    constructor() {
        this.test = {
            aaA: 'test',
            bBB: 1,
        };

        const testB: b = {
            aaA: 'test',
            bBB: 2,
        };

    }
}

export type Stringify<T> = {
    [K in keyof T]: T[K] extends string ? T[K] : string;
}

export class Test2 {
    public test: Stringify<a>;

    constructor() {
        this.test = {
            aa_a: 'test',
            bB_B: "dg",
        };

        const testB: b = {
            aaA: 'test',
            bBB: 2,
        };
    }
}