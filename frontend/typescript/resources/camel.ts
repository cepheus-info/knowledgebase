export type SourceType = {
    aa: number;
    Bb: string;
    ccDd: string;
    eeFf: number;
};

export type DestType = {
    aa: number;
    bb: string;
    ccDd: string;
    eeFf: number;
};

export type Camelcase<K extends string> = K extends `${infer Prefix}.*${infer Postfix}` ? `${Uncapitalize<Prefix>}${Capitalize<Postfix>}` : Uncapitalize<K>;

export type Camel<T> = {
    [K in keyof T as Camelcase<K & string>]: T[K];
};

export type CamelcaseKeys<T> = {
    [K in keyof T as Uncapitalize<K & string>]: T[K];
};

export class Main {
    test() {
        const hello: CamelcaseKeys<SourceType> = {
            aa: 1,
            bb: "bb",
            eeFf: 1,
            ccDd: "ccDd",
        };

        const hello2: DestType = hello;
    }
}